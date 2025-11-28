"""
Simple IP check via Thordata proxy network.

Usage:
    1. Copy .env.example to .env and fill in THORDATA_SCRAPER_TOKEN.
    2. Install dependencies: pip install -r requirements.txt
    3. Run: python examples/python/simple_ip_check.py
"""

import os

from dotenv import load_dotenv
from thordata import ThordataClient

load_dotenv()

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")

if not SCRAPER_TOKEN:
    raise RuntimeError("Please set THORDATA_SCRAPER_TOKEN in your .env file.")

# For simple proxy usage, public tokens are not required.
client = ThordataClient(
    scraper_token=SCRAPER_TOKEN,
    public_token="",
    public_key="",
)


def main() -> None:
    url = "http://httpbin.org/ip"
    print(f"Requesting IP via Thordata proxy: {url}")

    resp = client.get(url, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    print("Response JSON:", data)
    print("Origin IP (should be a Thordata proxy IP):", data.get("origin"))


if __name__ == "__main__":
    main()