"""
Geo-targeted request via Thordata proxy network.

This example shows how to send a request that appears to come from a specific
country/region (if your Thordata plan supports geo-targeting).

Usage:
    python examples/python/geo_targeting.py
"""

import os

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


def main() -> None:
    url = "https://ipinfo.thordata.com"
    country = "us"  # change to "de", "gb", etc. depending on your account

    print(f"Requesting {url} via Thordata proxy (country={country})")

    # Geo-targeting is typically done via query params or headers.
    # Here we demonstrate passing 'country' as a query param for illustration.
    resp = client.get(f"{url}?X-Thordata-Country={country}", timeout=30)
    resp.raise_for_status()

    data = resp.json()
    print("Response headers seen by httpbin.org:")
    for k, v in data.get("headers", {}).items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()