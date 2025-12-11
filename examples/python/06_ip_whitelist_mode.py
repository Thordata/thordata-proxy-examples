"""
06 - IP Whitelist Mode

Use Thordata proxy without embedding credentials in the URL.
Your server's IP must be added to the whitelist in the Dashboard.

Usage:
    1. Add your server's public IP to Thordata Dashboard
    2. Run: python 06_ip_whitelist_mode.py
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

PROXY_HOST = os.getenv("THORDATA_PROXY_HOST", "pr.thordata.net")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT", "9999")


def main():
    # No credentials in the proxy URL - authentication is by IP whitelist
    proxy_url = f"http://{PROXY_HOST}:{PROXY_PORT}"

    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    print("🔓 IP Whitelist Mode")
    print()
    print(f"   Proxy: {proxy_url}")
    print("   (No credentials - your IP must be whitelisted)")
    print()

    url = "https://httpbin.org/ip"
    print(f"🌐 Requesting: {url}")

    try:
        response = requests.get(url, proxies=proxies, timeout=30)
        response.raise_for_status()

        data = response.json()
        print()
        print(f"✅ Success!")
        print(f"   Proxy IP: {data.get('origin', 'Unknown')}")

    except requests.exceptions.ProxyError as e:
        print()
        print(f"❌ Proxy Error: {e}")
        print()
        print("   Make sure your IP is whitelisted in the Thordata Dashboard.")
        print("   Your current public IP can be found at: https://httpbin.org/ip")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()