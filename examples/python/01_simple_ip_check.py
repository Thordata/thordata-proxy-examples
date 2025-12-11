"""
01 - Simple IP Check via Thordata Proxy

The most basic example: send a request through Thordata proxy
and verify your IP has changed.

Usage:
    python 01_simple_ip_check.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from repo root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import ThordataClient

# Get credentials
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")

if not SCRAPER_TOKEN:
    print("❌ Error: Please set THORDATA_SCRAPER_TOKEN in your .env file")
    print("   Copy .env.example to .env and fill in your credentials")
    sys.exit(1)


def main():
    # Initialize client
    client = ThordataClient(scraper_token=SCRAPER_TOKEN)

    # Target URL that returns your IP
    url = "https://httpbin.org/ip"

    print(f"🌐 Requesting: {url}")
    print("   via Thordata proxy network...")
    print()

    try:
        response = client.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        origin_ip = data.get("origin", "Unknown")

        print(f"✅ Success!")
        print(f"   Your proxy IP: {origin_ip}")
        print()
        print("   This IP belongs to the Thordata proxy network,")
        print("   not your real IP address.")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()