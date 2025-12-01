"""
Concurrent requests via ThordataClient (thread-based concurrency).

Demonstrates how to send many HTTP requests in parallel using Thordata's
proxy network + ThreadPoolExecutor.

Usage:
    python examples/python/concurrent_requests.py
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from dotenv import load_dotenv
from thordata import ThordataClient

load_dotenv()

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")

if not SCRAPER_TOKEN:
    raise RuntimeError("Please set THORDATA_SCRAPER_TOKEN in your .env file.")


def fetch_ip(index: int) -> str:
    """Fetch IP via proxy in a single thread."""
    client = ThordataClient(
        scraper_token=SCRAPER_TOKEN,
        public_token="",
        public_key="",
    )

    url = "http://httpbin.org/ip"
    try:
        resp = client.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        origin = data.get("origin")
        print(f"[{index}] IP: {origin}")
        return origin
    except Exception as exc:
        print(f"[{index}] Error: {exc}")
        return "error"


def run_concurrent(n: int = 5) -> List[str]:
    """Run N requests in parallel using a thread pool."""
    results: List[str] = []
    with ThreadPoolExecutor(max_workers=n) as executor:
        future_to_idx = {executor.submit(fetch_ip, i): i for i in range(1, n + 1)}
        for future in as_completed(future_to_idx):
            results.append(future.result())
    return results


if __name__ == "__main__":
    print("Running 5 concurrent IP checks via Thordata proxy...")
    results = run_concurrent(5)
    print("Results:", results)