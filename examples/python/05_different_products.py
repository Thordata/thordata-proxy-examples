"""
05 - Different Proxy Products

Compare Residential, Mobile, and Datacenter proxies.
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

USERNAME = os.getenv("THORDATA_USERNAME")
PASSWORD = os.getenv("THORDATA_PASSWORD")


def main():
    if not USERNAME or not PASSWORD:
        print("❌ Error: Please set THORDATA_USERNAME and THORDATA_PASSWORD in .env")
        sys.exit(1)

    print("🔄 Proxy Product Comparison")
    print("=" * 60)
    print()

    products = [
        (ProxyProduct.RESIDENTIAL, "General scraping, geo-targeting"),
        (ProxyProduct.MOBILE, "Mobile-specific content, apps"),
        (ProxyProduct.DATACENTER, "High-speed, cost-effective"),
        (ProxyProduct.ISP, "Long-term sessions, static IPs"),
    ]

    for product, description in products:
        config = ProxyConfig(
            username=USERNAME,
            password=PASSWORD,
            product=product,
            country="us",
        )

        print(f"📦 {product.value.upper()}")
        print(f"   Port:        {config.port}")
        print(f"   Use case:    {description}")
        print(f"   Username:    {config.build_username()}")
        print(f"   Proxy URL:   {config.protocol}://...@{config.host}:{config.port}")
        print()

    print("=" * 60)
    print()
    print("💡 Tips:")
    print("   • Residential: Best success rate, appears as real users")
    print("   • Mobile: For mobile-only content and apps")
    print("   • Datacenter: Fastest, but easier to detect")
    print("   • ISP: Static IPs, great for accounts that need consistency")


if __name__ == "__main__":
    main()