"""
IP whitelist mode example for Thordata proxies.

In this mode, you:
  1) Add your server's IP address to the Thordata Dashboard "IP whitelist".
  2) Do NOT include username/password in the proxy URL.
  3) Simply connect to http://gate.thordata.com:22225 from that IP.

This is useful when you don't want to embed tokens/passwords in code.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

PROXY_HOST = os.getenv("THORDATA_PROXY_HOST", "gate.thordata.com")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT", "22225")

PROXY_URL = f"http://{PROXY_HOST}:{PROXY_PORT}"

proxies = {
    "http": PROXY_URL,
    "https": PROXY_URL,
}


def main() -> None:
    # This endpoint returns the IP address seen by the target site.
    target_url = "https://ipinfo.thordata.com"

    print("Using proxy:", PROXY_URL)
    print("Target URL:", target_url)
    print("Make sure your current machine IP is whitelisted in the Thordata Dashboard.")

    resp = requests.get(target_url, proxies=proxies, timeout=30)
    print("Status code:", resp.status_code)
    print("Response headers:", resp.headers)
    print("Response text:", resp.text)
    resp.raise_for_status()


if __name__ == "__main__":
    main()