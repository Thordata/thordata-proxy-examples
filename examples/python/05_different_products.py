"""
05 - Different Proxy Products

Compare Residential, Mobile, Datacenter, and ISP proxies.
Each product has different characteristics and use cases.

Usage:
    python 05_different_products.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import ProxyConfig, ProxyProduct

RESIDENTIAL_USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
RESIDENTIAL_PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")
PROXY_HOST = os.getenv("THORDATA_PROXY_HOST")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT")


def main():
    if not RESIDENTIAL_USERNAME or not RESIDENTIAL_PASSWORD:
        print("[ERROR] Error: Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in .env")
        sys.exit(1)

    print(" Proxy Product Comparison")
    print("=" * 60)
    print()

    products = [
        (ProxyProduct.RESIDENTIAL, "General scraping, geo-targeting"),
        (ProxyProduct.MOBILE, "Mobile-specific content, apps"),
        (ProxyProduct.DATACENTER, "High-speed, cost-effective"),
        (ProxyProduct.ISP, "Long-term sessions, static IPs"),
    ]

    for product, description in products:
        kwargs: dict = {
            "username": RESIDENTIAL_USERNAME,
            "password": RESIDENTIAL_PASSWORD,
            "product": product,
            "country": "us",
        }
        if PROXY_HOST:
            kwargs["host"] = PROXY_HOST
        if PROXY_PORT:
            try:
                kwargs["port"] = int(PROXY_PORT)
            except ValueError:
                pass

        config = ProxyConfig(**kwargs)

        print(f" {product.value.upper()}")
        print(f"   Port:        {config.port}")
        print(f"   Host:        {config.host}")
        print(f"   Use case:    {description}")
        print(f"   Username:    {config.build_username()}")
        print(f"   Endpoint:    {config.build_proxy_endpoint()}")
        print()

    print("=" * 60)
    print()
    print(" Tips:")
    print("   - Residential: Best success rate, appears as real users")
    print("   - Mobile: For mobile-only content and apps")
    print("   - Datacenter: Fastest, but easier to detect")
    print("   - ISP: Static IPs, great for accounts that need consistency")


if __name__ == "__main__":
    main()
