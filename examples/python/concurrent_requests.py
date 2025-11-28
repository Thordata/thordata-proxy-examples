"""
Concurrent requests via AsyncThordataClient.

Demonstrates how to send many HTTP requests in parallel using Thordata's
proxy network + asyncio.

Usage:
    python examples/python/concurrent_requests.py
"""

import asyncio
import os
from typing import List

from dotenv import load_dotenv
from thordata import AsyncThordataClient

load_dotenv()

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")

if not SCRAPER_TOKEN:
    raise RuntimeError("Please set THORDATA_SCRAPER_TOKEN in your .env file.")


async def fetch_ip(client: AsyncThordataClient, idx: int) -> str:
    url = "http://httpbin.org/ip"
    try:
        resp = await client.get(url, timeout=30)
        data = await resp.json()
        origin = data.get("origin")
        print(f"[{idx}] IP: {origin}")
        return origin
    except Exception as exc:
        print(f"[{idx}] Error: {exc}")
        return "error"


async def main_concurrent(n: int = 5) -> List[str]:
    async with AsyncThordataClient(
        scraper_token=SCRAPER_TOKEN,
        public_token="",
        public_key="",
    ) as client:
        tasks = [fetch_ip(client, i) for i in range(1, n + 1)]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    results = asyncio.run(main_concurrent(5))
    print("Results:", results)