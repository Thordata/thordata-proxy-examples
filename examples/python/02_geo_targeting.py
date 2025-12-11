"""
02 - Geo-Targeted Requests via Thordata Proxy

Send requests that appear to come from a specific location.
Uses the new ProxyConfig class from SDK v0.4.0.

Usage:
    python 02_geo_targeting.py
    python 02_geo_targeting.py --country de
    python 02_geo_targeting.py --country us --state california --city seattle
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import ThordataClient, ProxyConfig

# Get credentials
USERNAME = os.getenv("THORDATA_USERNAME")
PASSWORD = os.getenv("THORDATA_PASSWORD")
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Geo-targeted request via Thordata proxy"
    )
    parser.add_argument(
        "--country", "-c",
        default="us",
        help="Target country code (e.g., us, de, jp)"
    )
    parser.add_argument(
        "--state", "-s",
        default=None,
        help="Target state (e.g., california, texas)"
    )
    parser.add_argument(
        "--city",
        default=None,
        help="Target city (e.g., seattle, los_angeles)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not USERNAME or not PASSWORD:
        print("❌ Error: Please set THORDATA_USERNAME and THORDATA_PASSWORD in .env")
        sys.exit(1)

    # Build proxy configuration with geo-targeting
    proxy_config = ProxyConfig(
        username=USERNAME,
        password=PASSWORD,
        country=args.country,
        state=args.state,
        city=args.city,
    )

    # Show the generated proxy URL (without password)
    print(f"🌍 Geo-targeting configuration:")
    print(f"   Country: {args.country}")
    if args.state:
        print(f"   State:   {args.state}")
    if args.city:
        print(f"   City:    {args.city}")
    print()
    print(f"   Username: {proxy_config.build_username()}")
    print()

    # Initialize client (we'll use the proxy_config for the request)
    client = ThordataClient(scraper_token=SCRAPER_TOKEN or "dummy")

    # Request IP info
    url = "https://ipinfo.io/json"

    print(f"🌐 Requesting: {url}")

    try:
        response = client.get(url, proxy_config=proxy_config, timeout=30)
        response.raise_for_status()

        data = response.json()

        print()
        print(f"✅ Response:")
        print(f"   IP:      {data.get('ip', 'N/A')}")
        print(f"   Country: {data.get('country', 'N/A')}")
        print(f"   Region:  {data.get('region', 'N/A')}")
        print(f"   City:    {data.get('city', 'N/A')}")
        print(f"   Org:     {data.get('org', 'N/A')}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()