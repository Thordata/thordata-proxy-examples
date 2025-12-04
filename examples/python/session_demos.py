"""
Thordata Proxy Session Management Demo.

Demonstrates:
1. Rotating Session (default, new IP per request).
2. Sticky Session (keep IP via 'sessid-ID-sesstime-MIN' param).

Based on official docs:
  username format: user-USERNAME-sessid-ID-sesstime-MIN
  (or td-customer-USERNAME-sessid-ID-sesstime-MIN)

Usage:
    python examples/python/session_demos.py
"""

import os
import random
import string
import requests
from dotenv import load_dotenv

load_dotenv()

# In Thordata dashboard, this is your "Proxy Username" or "Scraper Token"
USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME") or os.getenv("THORDATA_SCRAPER_TOKEN")
PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD") or ""

if not USERNAME:
    raise RuntimeError("Please set THORDATA_RESIDENTIAL_USERNAME (or SCRAPER_TOKEN) in .env")

PROXY_HOST = os.getenv("THORDATA_RESIDENTIAL_HOST", "t.na.thordata.net")
PROXY_PORT = os.getenv("THORDATA_RESIDENTIAL_PORT", "9999")

# Use a simple plaintext IP echo service
TARGET_URL = "http://checkip.amazonaws.com"


def get_ip(session_id: str = None, session_time: int = 10, label: str = "") -> str:
    """
    Send a request with optional sticky session parameters.
    """
    user_str = USERNAME
    # Ensure correct prefix if missing (adjust based on your actual dashboard username format)
    if not user_str.startswith("td-customer-") and not user_str.startswith("user-"):
        # Some plans require 'td-customer-' prefix manually if not part of the token
        pass 

    # Construct sticky params
    if session_id:
        user_str += f"-sessid-{session_id}-sesstime-{session_time}"

    proxy_url = f"http://{user_str}:{PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
    
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    try:
        resp = requests.get(TARGET_URL, proxies=proxies, timeout=30)
        resp.raise_for_status()
        
        # checkip.amazonaws.com returns plain text IP
        ip = resp.text.strip()
            
        print(f"[{label}] Session: {session_id or 'Rotating'} -> IP: {ip}")
        return ip
    except Exception as e:
        print(f"[{label}] Error: {e}")
        return "error"


def demo_rotating():
    print("\n--- 1. Rotating IP Demo (Default) ---")
    ips = set()
    for i in range(3):
        ip = get_ip(session_id=None, label=f"Req {i+1}")
        if ip != "error":
            ips.add(ip)
    
    # In a perfect rotating world, we expect >1 unique IP.
    # But sometimes pools reuse IPs, so we just show what we got.
    print(f"Unique IPs: {len(ips)} / 3")


def demo_sticky():
    print("\n--- 2. Sticky IP Demo (sessid + sesstime) ---")
    
    # Generate a random 6-char session ID
    sess_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    print(f"Using Session ID: {sess_id} (Duration: 10 mins)")

    ips = set()
    for i in range(3):
        ip = get_ip(session_id=sess_id, session_time=10, label=f"Req {i+1}")
        if ip != "error":
            ips.add(ip)
    
    # In sticky mode, we expect exactly 1 unique IP (unless it went offline).
    print(f"Unique IPs: {len(ips)} / 3 (Expect 1)")


if __name__ == "__main__":
    demo_rotating()
    demo_sticky()