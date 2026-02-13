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

from thordata import ThordataClient, ProxyConfig, ProxyProduct

# Get credentials
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")
RESIDENTIAL_USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
RESIDENTIAL_PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")
PROXY_HOST = os.getenv("THORDATA_PROXY_HOST")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT")

if not SCRAPER_TOKEN:
    print("[ERROR] Please set THORDATA_SCRAPER_TOKEN in your .env file")
    print("   Copy .env.example to .env and fill in your credentials")
    sys.exit(1)

if not RESIDENTIAL_USERNAME or not RESIDENTIAL_PASSWORD:
    print("[ERROR] Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in your .env file")
    sys.exit(1)


def main():
    # Initialize client
    client = ThordataClient(scraper_token=SCRAPER_TOKEN)

    # Build proxy configuration (same as other examples)
    proxy_kwargs: dict = {
        "username": RESIDENTIAL_USERNAME,
        "password": RESIDENTIAL_PASSWORD,
        "product": ProxyProduct.RESIDENTIAL,
    }
    if PROXY_HOST:
        proxy_kwargs["host"] = PROXY_HOST
    if PROXY_PORT:
        try:
            proxy_kwargs["port"] = int(PROXY_PORT)
        except ValueError:
            pass

    proxy_config = ProxyConfig(**proxy_kwargs)

    # Target URL that returns your IP
    # Using ipinfo.io which is generally more stable in restricted networks
    url = "https://ipinfo.io/json"

    print(f"Requesting: {url}")
    print("   via Thordata proxy network...")
    print()

    try:
        response = client.get(url, proxy_config=proxy_config, timeout=30)
        response.raise_for_status()

        data = response.json()
        origin_ip = data.get("ip", data.get("origin", "Unknown"))

        print("[SUCCESS]")
        print(f"   Your proxy IP: {origin_ip}")
        print()
        print("   This IP belongs to the Thordata proxy network,")
        print("   not your real IP address.")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
