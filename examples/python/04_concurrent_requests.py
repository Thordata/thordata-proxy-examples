"""
04 - High-Concurrency Async Requests

Send multiple requests in parallel using AsyncThordataClient.
Demonstrates maximum throughput with the proxy network.

Usage:
    python 04_concurrent_requests.py
    python 04_concurrent_requests.py --count 20
"""

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import AsyncThordataClient, ThordataClient, ProxyConfig, ProxyProduct

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")
RESIDENTIAL_USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
RESIDENTIAL_PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")
PROXY_HOST = os.getenv("THORDATA_PROXY_HOST")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT")
UPSTREAM_PROXY = os.getenv("THORDATA_UPSTREAM_PROXY")


def parse_args():
    parser = argparse.ArgumentParser(description="Concurrent requests demo")
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=5,
        help="Number of concurrent requests"
    )
    return parser.parse_args()


async def fetch_ip_async(client: AsyncThordataClient, request_id: int) -> dict:
    """Fetch IP info for a single request using AsyncThordataClient."""
    url = "https://ipinfo.io/json"
    try:
        response = await client.get(url)
        data = await response.json()
        return {
            "id": request_id,
            "ip": data.get("ip", data.get("origin", "Unknown")),
            "status": "success",
        }
    except Exception as e:
        return {
            "id": request_id,
            "ip": None,
            "status": f"error: {e}",
        }


def build_proxy_config() -> ProxyConfig | None:
    """Build ProxyConfig from environment, if credentials are available."""
    if not RESIDENTIAL_USERNAME or not RESIDENTIAL_PASSWORD:
        return None

    kwargs: dict = {
        "username": RESIDENTIAL_USERNAME,
        "password": RESIDENTIAL_PASSWORD,
        "product": ProxyProduct.RESIDENTIAL,
    }
    if PROXY_HOST:
        kwargs["host"] = PROXY_HOST
    if PROXY_PORT:
        try:
            kwargs["port"] = int(PROXY_PORT)
        except ValueError:
            pass

    return ProxyConfig(**kwargs)


def fetch_ip_sync(request_id: int, proxy_config: ProxyConfig | None) -> dict:
    """Fetch IP info for a single request using sync ThordataClient (for upstream proxy)."""
    client = ThordataClient(scraper_token=SCRAPER_TOKEN)
    url = "https://ipinfo.io/json"
    try:
        response = client.get(url, proxy_config=proxy_config, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {
            "id": request_id,
            "ip": data.get("ip", data.get("origin", "Unknown")),
            "status": "success",
        }
    except Exception as e:
        return {
            "id": request_id,
            "ip": None,
            "status": f"error: {e}",
        }


async def main():
    args = parse_args()

    if not SCRAPER_TOKEN:
        print("[ERROR] Error: Please set THORDATA_SCRAPER_TOKEN in .env")
        sys.exit(1)

    print(f" Sending {args.count} concurrent requests...")
    print()

    start_time = time.time()

    # If upstream proxy is configured, AsyncThordataClient currently has
    # limitations with HTTPS proxies. In that case, use sync client in threads.
    use_sync_threads = bool(UPSTREAM_PROXY)
    results: list[dict]

    if use_sync_threads:
        print(" Note: THORDATA_UPSTREAM_PROXY is set; using sync ThordataClient in threads.")
        proxy_config = build_proxy_config()
        if proxy_config is None:
            print("[ERROR] THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD are required for this demo.")
            sys.exit(1)

        tasks = [
            asyncio.to_thread(fetch_ip_sync, i + 1, proxy_config)
            for i in range(args.count)
        ]
        results = await asyncio.gather(*tasks)
    else:
        async with AsyncThordataClient(scraper_token=SCRAPER_TOKEN) as client:
            tasks = [
                fetch_ip_async(client, i + 1)
                for i in range(args.count)
            ]
            results = await asyncio.gather(*tasks)

    elapsed = time.time() - start_time

    # Display results
    success_count = 0
    unique_ips = set()

    for result in results:
        status_icon = "[SUCCESS]" if result["status"] == "success" else "[ERROR]"
        print(f"   {status_icon} Request {result['id']:2d}: {result['ip'] or result['status']}")
        
        if result["status"] == "success":
            success_count += 1
            unique_ips.add(result["ip"])

    print()
    print(f" Summary:")
    print(f"   Total requests:  {args.count}")
    print(f"   Successful:      {success_count}")
    print(f"   Unique IPs:      {len(unique_ips)}")
    print(f"   Total time:      {elapsed:.2f}s")
    print(f"   Requests/second: {args.count / elapsed:.1f}")


if __name__ == "__main__":
    asyncio.run(main())
