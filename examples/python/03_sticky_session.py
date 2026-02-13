"""
03 - Sticky Session (Same IP for Multiple Requests)

Maintain the same proxy IP across multiple requests using sticky sessions.
Useful for multi-step operations that require IP consistency.

Usage:
    python 03_sticky_session.py
    python 03_sticky_session.py --duration 15 --requests 5
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import ThordataClient, StickySession

RESIDENTIAL_USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
RESIDENTIAL_PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")
PROXY_HOST = os.getenv("THORDATA_PROXY_HOST")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT")


def parse_args():
    parser = argparse.ArgumentParser(description="Sticky session demo")
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=10,
        help="Session duration in minutes (1-90)"
    )
    parser.add_argument(
        "--requests", "-n",
        type=int,
        default=3,
        help="Number of requests to make"
    )
    parser.add_argument(
        "--country", "-c",
        default="us",
        help="Target country"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not RESIDENTIAL_USERNAME or not RESIDENTIAL_PASSWORD:
        print("[ERROR] Error: Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in .env")
        sys.exit(1)

    if not SCRAPER_TOKEN:
        print("[ERROR] Error: Please set THORDATA_SCRAPER_TOKEN in .env")
        sys.exit(1)

    # Create a sticky session
    # This automatically generates a session ID and sets the duration
    sticky_kwargs: dict = {
        "username": RESIDENTIAL_USERNAME,
        "password": RESIDENTIAL_PASSWORD,
        "country": args.country,
        "duration_minutes": args.duration,
    }
    if PROXY_HOST:
        sticky_kwargs["host"] = PROXY_HOST
    if PROXY_PORT:
        try:
            sticky_kwargs["port"] = int(PROXY_PORT)
        except ValueError:
            pass

    session = StickySession(**sticky_kwargs)

    print(f" Sticky Session Configuration:")
    print(f"   Session ID: {session.session_id}")
    print(f"   Duration:   {args.duration} minutes")
    print(f"   Country:    {args.country}")
    print()

    client = ThordataClient(scraper_token=SCRAPER_TOKEN)
    url = "https://httpbin.org/ip"

    print(f" Making {args.requests} requests (should all show same IP):")
    print()

    ips = []
    for i in range(args.requests):
        try:
            response = client.get(url, proxy_config=session, timeout=30)
            response.raise_for_status()
            
            ip = response.json().get("origin", "Unknown")
            ips.append(ip)
            print(f"   Request {i+1}: {ip}")

        except Exception as e:
            print(f"   Request {i+1}: [ERROR] Error - {e}")

    print()

    # Verify all IPs are the same
    unique_ips = set(ips)
    if len(unique_ips) == 1:
        print(f"[SUCCESS] Success! All {len(ips)} requests used the same IP: {ips[0]}")
    else:
        print(f"[WARNING]  Warning: Got {len(unique_ips)} different IPs: {unique_ips}")
        print("   This might happen if the session expired or there was an error.")


if __name__ == "__main__":
    main()
