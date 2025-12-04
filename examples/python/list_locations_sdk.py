"""
List locations using Thordata Python SDK.

This example uses the ThordataClient methods:
- list_countries(proxy_type)
- list_states(country_code, proxy_type)
- list_cities(country_code, state_code, proxy_type)
- list_asn(country_code, proxy_type)

Note:
    proxy_type=1  -> Residential proxies
    proxy_type=2  -> High-bandwidth / Unlimited proxies

Usage (from repo root):

    # Default: residential proxies (proxy_type=1), country=US, state=alabama
    python examples/python/list_locations_sdk.py

    # High-bandwidth proxies (proxy_type=2) and a different country:
    python examples/python/list_locations_sdk.py --proxy-type 2 --country DE
"""

from __future__ import annotations

import argparse
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List Thordata proxy locations via SDK.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--proxy-type",
        type=int,
        default=1,
        choices=(1, 2),
        help="Proxy type: 1 = residential, 2 = high-bandwidth/unlimited.",
    )
    parser.add_argument(
        "--country",
        type=str,
        default="US",
        help="Country code to use for states/cities/ASN (e.g. 'US', 'DE').",
    )
    parser.add_argument(
        "--state",
        type=str,
        default="alabama",
        help="State code to use when listing cities (e.g. 'alabama').",
    )
    return parser.parse_args()


def print_sample(title: str, rows: List[Dict], fields: List[str], limit: int = 10) -> None:
    print(f"\n{title} (first {min(len(rows), limit)} of {len(rows)}):")
    for row in rows[:limit]:
        line = " | ".join(str(row.get(f, "")) for f in fields)
        print("  " + line)


def main() -> None:
    args = parse_args()
    proxy_type = args.proxy_type
    country_code = args.country.upper()
    state_code = args.state

    print(f"Using proxy_type={proxy_type} (1=residential, 2=high-bandwidth)")
    print(f"Country={country_code}, state={state_code}")

    # 1. Countries
    countries = client.list_countries(proxy_type=proxy_type)
    print_sample("Countries", countries, ["country_code", "country_name"])

    # 2. States in the selected country
    states = client.list_states(country_code=country_code, proxy_type=proxy_type)
    print_sample(f"{country_code} States", states, ["state_code", "state_name"])

    # 3. Cities in the selected state
    cities = client.list_cities(
        country_code=country_code,
        state_code=state_code,
        proxy_type=proxy_type,
    )
    print_sample(f"{country_code} Cities in '{state_code}'", cities, ["city_code", "city_name"])

    # 4. ASNs in the selected country
    asn_list = client.list_asn(country_code=country_code, proxy_type=proxy_type)
    print_sample(f"{country_code} ASN", asn_list, ["asn_code", "asn_name"])


if __name__ == "__main__":
    main()