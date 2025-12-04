"""
Geo-targeted request via Thordata proxy network.

This example shows how to send a request that appears to come from a specific
country/region (if your Thordata plan supports geo-targeting).

We call https://ipinfo.thordata.com via the Thordata proxy and instruct the
gateway to use a specific country, so that the reported IP/location reflect
that geo-targeting.

Usage (from repo root):

    # Default: country=us
    python examples/python/geo_targeting.py

    # Custom country:
    python examples/python/geo_targeting.py --country de
"""

from __future__ import annotations

import argparse
import os
from typing import Any, Dict

from dotenv import load_dotenv
from thordata import ThordataClient

load_dotenv()

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")

if not SCRAPER_TOKEN:
    raise RuntimeError("Please set THORDATA_SCRAPER_TOKEN in your .env file.")

client = ThordataClient(
    scraper_token=SCRAPER_TOKEN,
    public_token="",
    public_key="",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Geo-targeted IP info via Thordata proxy.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--country",
        "-c",
        type=str,
        default="us",
        help="Target country code (e.g. 'us', 'de', 'fr').",
    )
    return parser.parse_args()


def pretty_print_ipinfo(data: Dict[str, Any]) -> None:
    """
    Pretty-print a typical ipinfo-style JSON response.

    We don't rely on a strict schema here; we just try common keys.
    """
    ip = data.get("ip")
    country = data.get("country") or data.get("country_name")
    region = data.get("region") or data.get("state")
    city = data.get("city")

    print("IP info JSON:", data)
    print("\nParsed fields:")
    print(f"  IP      : {ip}")
    print(f"  Country : {country}")
    print(f"  Region  : {region}")
    print(f"  City    : {city}")


def main() -> None:
    args = parse_args()

    url = "https://ipinfo.thordata.com"
    country = args.country.lower()

    print(f"Requesting {url} via Thordata proxy (country={country})")

    # Geo-targeting is implemented on the Thordata gateway side.
    # Here we demonstrate passing 'X-Thordata-Country' as a query parameter.
    params = {"X-Thordata-Country": country}

    resp = client.get(url, params=params, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    pretty_print_ipinfo(data)


if __name__ == "__main__":
    main()