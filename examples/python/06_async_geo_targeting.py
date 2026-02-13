"""
06 - Async Geo-Targeting with ProxyConfig

Demonstrate async requests with geo-targeting using ProxyConfig.
Shows how to efficiently make multiple geo-targeted requests in parallel.

Usage:
    python 06_async_geo_targeting.py
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import AsyncThordataClient, ProxyConfig, ProxyProduct

RESIDENTIAL_USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
RESIDENTIAL_PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")
PROXY_HOST = os.getenv("THORDATA_PROXY_HOST")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT")


async def fetch_location_info(client: AsyncThordataClient, country: str, proxy_config: ProxyConfig) -> dict:
    """Fetch location info for a specific country."""
    url = "https://ipinfo.io/json"
    try:
        response = await client.get(url, proxy_config=proxy_config, timeout=30)
        data = await response.json()
        return {
            "country": country,
            "ip": data.get("ip", "N/A"),
            "city": data.get("city", "N/A"),
            "region": data.get("region", "N/A"),
            "status": "success"
        }
    except Exception as e:
        return {
            "country": country,
            "status": f"error: {e}"
        }


async def main():
    if not RESIDENTIAL_USERNAME or not RESIDENTIAL_PASSWORD:
        print("[ERROR] Error: Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in .env")
        sys.exit(1)

    if not SCRAPER_TOKEN:
        print("[ERROR] Error: Please set THORDATA_SCRAPER_TOKEN in .env")
        sys.exit(1)

    # Target countries
    countries = ["us", "de", "jp", "gb", "fr"]

    print(f" Fetching IP info from {len(countries)} countries concurrently...")
    print()

    async with AsyncThordataClient(scraper_token=SCRAPER_TOKEN) as client:
        # Create proxy configs and tasks for each country
        tasks = []
        for country in countries:
            kwargs: dict = {
                "username": RESIDENTIAL_USERNAME,
                "password": RESIDENTIAL_PASSWORD,
                "product": ProxyProduct.RESIDENTIAL,
                "country": country,
            }
            if PROXY_HOST:
                kwargs["host"] = PROXY_HOST
            if PROXY_PORT:
                try:
                    kwargs["port"] = int(PROXY_PORT)
                except ValueError:
                    pass

            proxy_config = ProxyConfig(**kwargs)
            tasks.append(fetch_location_info(client, country, proxy_config))

        # Execute all concurrently
        results = await asyncio.gather(*tasks)

    # Display results
    print("[SUCCESS] Results:")
    print()
    for result in results:
        if result["status"] == "success":
            print(f"   {result['country'].upper()}: {result['ip']} ({result['city']}, {result['region']})")
        else:
            print(f"   {result['country'].upper()}: [ERROR] {result['status']}")


if __name__ == "__main__":
    asyncio.run(main())
