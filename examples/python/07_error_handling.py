"""
07 - Proper Error Handling

Demonstrates how to handle various errors when using Thordata proxies.

Usage:
    python 07_error_handling.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import (
    ThordataClient,
    ProxyConfig,
    ThordataError,
    ThordataAuthError,
    ThordataRateLimitError,
    ThordataNetworkError,
    ThordataTimeoutError,
)

USERNAME = os.getenv("THORDATA_USERNAME")
PASSWORD = os.getenv("THORDATA_PASSWORD")
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")


def demo_error_handling():
    """Demonstrate proper error handling patterns."""
    
    print("🛡️ Error Handling Demo")
    print("=" * 60)
    print()

    if not SCRAPER_TOKEN:
        print("❌ Error: Please set THORDATA_SCRAPER_TOKEN in .env")
        return

    client = ThordataClient(scraper_token=SCRAPER_TOKEN)

    # Example 1: Successful request
    print("1️⃣ Normal request (should succeed):")
    try:
        response = client.get("https://httpbin.org/ip", timeout=30)
        response.raise_for_status()
        print(f"   ✅ Success: {response.json()}")
    except ThordataError as e:
        print(f"   ❌ Error: {e}")
    print()

    # Example 2: Handling timeout
    print("2️⃣ Request with very short timeout (may timeout):")
    try:
        response = client.get("https://httpbin.org/delay/5", timeout=1)
        print(f"   ✅ Success (surprisingly fast!)")
    except ThordataTimeoutError as e:
        print(f"   ⏱️ Timeout (expected): {e}")
    except ThordataError as e:
        print(f"   ❌ Other error: {e}")
    print()

    # Example 3: Error hierarchy
    print("3️⃣ Error handling hierarchy:")
    print("""
    try:
        response = client.get(url)
    except ThordataAuthError as e:
        # 401/403 - Check your credentials
        print(f"Auth failed: {e}")
    except ThordataRateLimitError as e:
        # 429 - Too many requests, wait and retry
        print(f"Rate limited. Retry after: {e.retry_after}s")
    except ThordataTimeoutError as e:
        # Request timed out - retry with longer timeout
        print(f"Timeout: {e}")
    except ThordataNetworkError as e:
        # Network issue - check connection
        print(f"Network error: {e}")
    except ThordataError as e:
        # Catch-all for other Thordata errors
        print(f"Thordata error: {e}")
    except Exception as e:
        # Catch-all for non-Thordata errors
        print(f"Unexpected error: {e}")
    """)

    print("=" * 60)
    print()
    print("💡 Best Practices:")
    print("   • Always set appropriate timeouts")
    print("   • Catch specific exceptions before generic ones")
    print("   • Implement retry logic for transient errors")
    print("   • Log errors for debugging")


if __name__ == "__main__":
    demo_error_handling()