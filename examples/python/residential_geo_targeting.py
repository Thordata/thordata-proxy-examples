"""
Residential proxy geo-targeting examples using Thordata.

This script demonstrates how to construct proxy usernames according to the docs:

- Country:   td-customer-USERNAME-country-us
- State:     td-customer-USERNAME-country-us-state-california
- City:      td-customer-USERNAME-country-us-city-houston
- Continent: td-customer-USERNAME-continent-as
- ASN:       td-customer-USERNAME-country-fr-asn-AS12322

Usage:

    1. Copy .env.example to .env and fill in:

           THORDATA_RESIDENTIAL_USERNAME=your_sub_user_name
           THORDATA_RESIDENTIAL_PASSWORD=your_password

    2. Install deps: pip install -r requirements.txt
    3. Run:

           python examples/python/residential_geo_targeting.py
"""

import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")

if not USERNAME or not PASSWORD:
    raise RuntimeError(
        "Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD "
        "in your .env file."
    )


PROXY_HOST = os.getenv("THORDATA_RESIDENTIAL_HOST", "t.na.thordata.net:9999")

TARGET_URL = "https://ipinfo.thordata.com"


def build_proxy_username(
    username: str,
    country: str | None = None,
    state: str | None = None,
    city: str | None = None,
    continent: str | None = None,
    asn: str | None = None,
) -> str:
    """
    Build proxy username according to Thordata docs.

    Examples:
        td-customer-USERNAME-country-us
        td-customer-USERNAME-country-us-state-california
        td-customer-USERNAME-country-us-city-houston
        td-customer-USERNAME-continent-as
        td-customer-USERNAME-country-fr-asn-AS12322
    """
    parts = [f"td-customer-{username}"]

    # continent-level
    if continent:
        parts.append(f"continent-{continent.lower()}")

    # country-level
    if country:
        parts.append(f"country-{country.lower()}")

    # state-level (must be used with country)
    if state:
        parts.append(f"state-{state.lower()}")

    # city-level (must be used with country)
    if city:
        parts.append(f"city-{city.lower()}")

    # ASN (must be used with country)
    if asn:
        parts.append(f"asn-{asn}")

    return "-".join(parts)


def request_with_proxy(proxy_username: str) -> None:
    proxy_url = f"https://{proxy_username}:{PASSWORD}@{PROXY_HOST}"
    proxies: Dict[str, str] = {
        "http": proxy_url,
        "https": proxy_url,
    }

    print(f"\nUsing proxy username: {proxy_username}")
    print(f"Proxy server: {PROXY_HOST}")
    resp = requests.get(TARGET_URL, proxies=proxies, timeout=30)
    resp.raise_for_status()
    print("Response:", resp.text)


def main() -> None:
    # 1. Country-level example (US)
    proxy_user_country = build_proxy_username(USERNAME, country="us")
    request_with_proxy(proxy_user_country)

    # 2. Country + state example (US-California)
    proxy_user_state = build_proxy_username(
        USERNAME,
        country="us",
        state="california",
    )
    request_with_proxy(proxy_user_state)

    # 3. Country + city example (US-Houston)
    proxy_user_city = build_proxy_username(
        USERNAME,
        country="us",
        city="houston",
    )
    request_with_proxy(proxy_user_city)

    # 4. Continent example (Asia)
    proxy_user_continent = build_proxy_username(
        USERNAME,
        continent="as",  # Asia
    )
    request_with_proxy(proxy_user_continent)

    # 5. ASN example (France, AS12322 for Free SAS)
    proxy_user_asn = build_proxy_username(
        USERNAME,
        country="fr",
        asn="AS12322",
    )
    request_with_proxy(proxy_user_asn)


if __name__ == "__main__":
    main()