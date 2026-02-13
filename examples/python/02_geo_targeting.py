"""
02 - Geo-Targeted Requests via Thordata Proxy

Send requests that appear to come from a specific location.
Uses ProxyConfig for flexible geo-targeting.

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

from thordata import ThordataClient, ProxyConfig, ProxyProduct

# Get credentials (residential proxy user)
RESIDENTIAL_USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
RESIDENTIAL_PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")
PROXY_HOST = os.getenv("THORDATA_PROXY_HOST")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT")


def parse_args():
    parser = argparse.ArgumentParser(description="Geo-targeted request via Thordata proxy")
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
    parser.add_argument(
        "--product", "-p",
        choices=["residential", "mobile", "datacenter", "isp"],
        default="residential",
        help="Proxy product type"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not RESIDENTIAL_USERNAME or not RESIDENTIAL_PASSWORD:
        print("[ERROR] Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in .env")
        sys.exit(1)

    if not SCRAPER_TOKEN:
        print("[ERROR] Please set THORDATA_SCRAPER_TOKEN in .env")
        sys.exit(1)

    # Build proxy configuration with geo-targeting
    proxy_kwargs: dict = {
        "username": RESIDENTIAL_USERNAME,
        "password": RESIDENTIAL_PASSWORD,
        "product": ProxyProduct(args.product),
        "country": args.country,
        "state": args.state,
        "city": args.city,
    }
    if PROXY_HOST:
        proxy_kwargs["host"] = PROXY_HOST
    if PROXY_PORT:
        try:
            proxy_kwargs["port"] = int(PROXY_PORT)
        except ValueError:
            pass

    proxy_config = ProxyConfig(**proxy_kwargs)

    # Show the generated proxy configuration
    print(f"Geo-targeting configuration:")
    print(f"   Product: {args.product}")
    print(f"   Country: {args.country}")
    if args.state:
        print(f"   State:   {args.state}")
    if args.city:
        print(f"   City:    {args.city}")
    print()
    print(f"   Username: {proxy_config.build_username()}")
    print(f"   Endpoint: {proxy_config.build_proxy_endpoint()}")
    print()

    # Initialize client
    client = ThordataClient(scraper_token=SCRAPER_TOKEN)

    # Request IP info
    url = "https://ipinfo.io/json"

    print(f"Requesting: {url}")

    try:
        response = client.get(url, proxy_config=proxy_config, timeout=30)
        response.raise_for_status()

        data = response.json()

        print()
        print(f"[SUCCESS] Response:")
        print(f"   IP:      {data.get('ip', 'N/A')}")
        print(f"   Country: {data.get('country', 'N/A')}")
        print(f"   Region:  {data.get('region', 'N/A')}")
        print(f"   City:    {data.get('city', 'N/A')}")
        print(f"   Org:     {data.get('org', 'N/A')}")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
