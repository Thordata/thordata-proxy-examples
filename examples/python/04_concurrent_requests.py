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

from thordata import AsyncThordataClient

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")


def parse_args():
    parser = argparse.ArgumentParser(description="Concurrent requests demo")
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=10,
        help="Number of concurrent requests"
    )
    return parser.parse_args()


async def fetch_ip(client: AsyncThordataClient, request_id: int) -> dict:
    """Fetch IP info for a single request."""
    url = "https://httpbin.org/ip"
    try:
        response = await client.get(url)
        data = await response.json()
        return {
            "id": request_id,
            "ip": data.get("origin", "Unknown"),
            "status": "success"
        }
    except Exception as e:
        return {
            "id": request_id,
            "ip": None,
            "status": f"error: {e}"
        }


async def main():
    args = parse_args()

    if not SCRAPER_TOKEN:
        print("❌ Error: Please set THORDATA_SCRAPER_TOKEN in .env")
        sys.exit(1)

    print(f"🚀 Sending {args.count} concurrent requests...")
    print()

    start_time = time.time()

    async with AsyncThordataClient(scraper_token=SCRAPER_TOKEN) as client:
        # Create all tasks
        tasks = [
            fetch_ip(client, i + 1)
            for i in range(args.count)
        ]

        # Execute all concurrently
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start_time

    # Display results
    success_count = 0
    unique_ips = set()

    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"   {status_icon} Request {result['id']:2d}: {result['ip'] or result['status']}")
        
        if result["status"] == "success":
            success_count += 1
            unique_ips.add(result["ip"])

    print()
    print(f"📊 Summary:")
    print(f"   Total requests:  {args.count}")
    print(f"   Successful:      {success_count}")
    print(f"   Unique IPs:      {len(unique_ips)}")
    print(f"   Total time:      {elapsed:.2f}s")
    print(f"   Requests/second: {args.count / elapsed:.1f}")


if __name__ == "__main__":
    asyncio.run(main())