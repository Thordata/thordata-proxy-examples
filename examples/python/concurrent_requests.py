"""
Concurrent requests via ThordataClient (thread-based concurrency).

Demonstrates how to send many HTTP requests in parallel using Thordata's
proxy network + ThreadPoolExecutor.

Usage (from repo root):

    # Default: 5 requests, 5 worker threads, target httpbin.org/ip
    python examples/python/concurrent_requests.py

    # Custom settings:
    python examples/python/concurrent_requests.py \
        --total 20 \
        --max-workers 10 \
        --url "http://httpbin.org/ip"
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

from dotenv import load_dotenv
from thordata import ThordataClient

load_dotenv()

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")

if not SCRAPER_TOKEN:
    raise RuntimeError("Please set THORDATA_SCRAPER_TOKEN in your .env file.")


def build_client() -> ThordataClient:
    """
    Build a new ThordataClient instance.

    Note:
      For simple IP-check use cases we don't need PUBLIC_TOKEN / PUBLIC_KEY.
      Each thread constructs its own client to avoid sharing sessions across
      threads.
    """
    return ThordataClient(
        scraper_token=SCRAPER_TOKEN,
        public_token="",
        public_key="",
    )


def fetch_ip(index: int, url: str) -> Tuple[int, str]:
    """
    Fetch IP via proxy in a single thread.

    Returns:
        (index, origin_ip_or_error)
    """
    client = build_client()
    try:
        resp = client.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        origin = data.get("origin") or data.get("ip") or str(data)
        print(f"[{index}] IP: {origin}")
        return index, origin
    except Exception as exc:
        print(f"[{index}] Error: {exc}")
        return index, "error"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Concurrent IP checks via Thordata proxy (thread-based).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--total",
        type=int,
        default=5,
        help="Total number of requests to send.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=None,
        help="Maximum number of worker threads. "
             "Defaults to --total if not set.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://httpbin.org/ip",
        help="Target URL that returns your visible IP.",
    )
    return parser.parse_args()


def run_concurrent(total: int, max_workers: int, url: str) -> List[str]:
    """Run N requests in parallel using a thread pool."""
    results: List[str] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(fetch_ip, i, url): i for i in range(1, total + 1)
        }
        for future in as_completed(future_to_idx):
            _, ip = future.result()
            results.append(ip)
    return results


def main() -> None:
    args = parse_args()

    total = max(1, args.total)
    max_workers = args.max_workers or total
    max_workers = max(1, max_workers)

    print(
        f"Running {total} concurrent IP checks via Thordata proxy "
        f"({max_workers} worker threads)..."
    )
    print(f"Target URL: {args.url}")

    t0 = time.perf_counter()
    results = run_concurrent(total, max_workers, args.url)
    elapsed = time.perf_counter() - t0

    unique_ips = {ip for ip in results if ip not in {"", "error"}}
    errors = sum(1 for ip in results if ip == "error")

    print("\nSummary:")
    print(f"  Total requests : {total}")
    print(f"  Unique IPs     : {len(unique_ips)} -> {unique_ips}")
    print(f"  Errors         : {errors}")
    print(f"  Elapsed time   : {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()