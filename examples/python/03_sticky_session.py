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

USERNAME = os.getenv("THORDATA_USERNAME")
PASSWORD = os.getenv("THORDATA_PASSWORD")
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")


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

    if not USERNAME or not PASSWORD:
        print("❌ Error: Please set THORDATA_USERNAME and THORDATA_PASSWORD in .env")
        sys.exit(1)

    # Create a sticky session
    # This automatically generates a session ID and sets the duration
    session = StickySession(
        username=USERNAME,
        password=PASSWORD,
        country=args.country,
        duration_minutes=args.duration,
    )

    print(f"🔒 Sticky Session Configuration:")
    print(f"   Session ID: {session.session_id}")
    print(f"   Duration:   {args.duration} minutes")
    print(f"   Country:    {args.country}")
    print()

    client = ThordataClient(scraper_token=SCRAPER_TOKEN or "dummy")
    url = "https://httpbin.org/ip"

    print(f"📡 Making {args.requests} requests (should all show same IP):")
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
            print(f"   Request {i+1}: ❌ Error - {e}")

    print()

    # Verify all IPs are the same
    unique_ips = set(ips)
    if len(unique_ips) == 1:
        print(f"✅ Success! All {len(ips)} requests used the same IP: {ips[0]}")
    else:
        print(f"⚠️  Warning: Got {len(unique_ips)} different IPs: {unique_ips}")
        print("   This might happen if the session expired or there was an error.")


if __name__ == "__main__":
    main()