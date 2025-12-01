"""
List locations using Thordata Python SDK.

This example uses the new ThordataClient methods:
- list_countries()
- list_states(country_code)
- list_cities(country_code, state_code)
- list_asn(country_code)

Usage:
    1. Ensure .env contains THORDATA_SCRAPER_TOKEN, THORDATA_PUBLIC_TOKEN, THORDATA_PUBLIC_KEY.
    2. Install deps: pip install -r requirements.txt
    3. Run:
        python examples/python/list_locations_sdk.py
"""

import os
from typing import List, Dict

from dotenv import load_dotenv
from thordata import ThordataClient

load_dotenv()

SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")
PUBLIC_TOKEN = os.getenv("THORDATA_PUBLIC_TOKEN")
PUBLIC_KEY = os.getenv("THORDATA_PUBLIC_KEY")

if not SCRAPER_TOKEN or not PUBLIC_TOKEN or not PUBLIC_KEY:
    raise RuntimeError(
        "Please set THORDATA_SCRAPER_TOKEN, THORDATA_PUBLIC_TOKEN and "
        "THORDATA_PUBLIC_KEY in your .env file."
    )

client = ThordataClient(
    scraper_token=SCRAPER_TOKEN,
    public_token=PUBLIC_TOKEN,
    public_key=PUBLIC_KEY,
)


def print_sample(title: str, rows: List[Dict], fields: List[str], limit: int = 10) -> None:
    print(f"\n{title} (first {min(len(rows), limit)}):")
    for row in rows[:limit]:
        line = " | ".join(str(row.get(f, "")) for f in fields)
        print("  " + line)


def main() -> None:
    # 1. Countries
    countries = client.list_countries(proxy_type=1)  # 1 = residential
    print_sample("Countries", countries, ["country_code", "country_name"])

    # 2. US states
    us_states = client.list_states(country_code="US", proxy_type=1)
    print_sample("US States", us_states, ["state_code", "state_name"])

    # 3. US cities in 'alabama'
    us_cities = client.list_cities(country_code="US", state_code="alabama", proxy_type=1)
    print_sample("US Cities in 'alabama'", us_cities, ["city_code", "city_name"])

    # 4. US ASNs
    us_asn = client.list_asn(country_code="US", proxy_type=1)
    print_sample("US ASN", us_asn, ["asn_code", "asn_name"])


if __name__ == "__main__":
    main()