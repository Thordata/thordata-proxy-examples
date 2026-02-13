"""
07 - Error Handling and Retry Logic

Demonstrate proper error handling patterns when using Thordata proxy.
Shows how to handle network errors, timeouts, and proxy failures.

Usage:
    python 07_error_handling.py
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from thordata import ThordataClient, ProxyConfig, ProxyProduct
from thordata.exceptions import ThordataError, ThordataNetworkError, ThordataTimeoutError

RESIDENTIAL_USERNAME = os.getenv("THORDATA_RESIDENTIAL_USERNAME")
RESIDENTIAL_PASSWORD = os.getenv("THORDATA_RESIDENTIAL_PASSWORD")
SCRAPER_TOKEN = os.getenv("THORDATA_SCRAPER_TOKEN")
PROXY_HOST = os.getenv("THORDATA_PROXY_HOST")
PROXY_PORT = os.getenv("THORDATA_PROXY_PORT")


def make_request_with_retry(client: ThordataClient, url: str, proxy_config: ProxyConfig, max_retries: int = 3) -> dict:
    """Make a request with retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"   Attempt {attempt}/{max_retries}...", end=" ")
            response = client.get(url, proxy_config=proxy_config, timeout=10)
            response.raise_for_status()
            data = response.json()
            print("[SUCCESS] Success")
            return {"success": True, "data": data, "attempts": attempt}

        except ThordataTimeoutError as e:
            print(f"[TIMEOUT]  Timeout: {e}")
            if attempt < max_retries:
                wait_time = attempt * 2
                print(f"      Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        except ThordataNetworkError as e:
            print(f" Network Error: {e}")
            if attempt < max_retries:
                wait_time = attempt * 2
                print(f"      Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        except ThordataError as e:
            print(f"[ERROR] Thordata Error: {e}")
            return {"success": False, "error": str(e), "attempts": attempt}

        except Exception as e:
            print(f"[ERROR] Unexpected Error: {e}")
            return {"success": False, "error": str(e), "attempts": attempt}

    return {"success": False, "error": "Max retries exceeded", "attempts": max_retries}


def main():
    if not RESIDENTIAL_USERNAME or not RESIDENTIAL_PASSWORD:
        print("[ERROR] Error: Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in .env")
        sys.exit(1)

    if not SCRAPER_TOKEN:
        print("[ERROR] Error: Please set THORDATA_SCRAPER_TOKEN in .env")
        sys.exit(1)

    client = ThordataClient(scraper_token=SCRAPER_TOKEN)
    kwargs: dict = {
        "username": RESIDENTIAL_USERNAME,
        "password": RESIDENTIAL_PASSWORD,
        "product": ProxyProduct.RESIDENTIAL,
        "country": "us",
    }
    if PROXY_HOST:
        kwargs["host"] = PROXY_HOST
    if PROXY_PORT:
        try:
            kwargs["port"] = int(PROXY_PORT)
        except ValueError:
            pass

    proxy_config = ProxyConfig(**kwargs)

    print("  Error Handling Demo")
    print("=" * 60)
    print()

    # Test 1: Normal request (using ipinfo.io for stability)
    print("Test 1: Normal request")
    url = "https://ipinfo.io/json"
    result = make_request_with_retry(client, url, proxy_config)
    if result["success"]:
        print(f"   IP: {result['data'].get('ip', result['data'].get('origin', 'N/A'))}")
    print()

    # Test 2: Request with very short timeout (will likely fail)
    print("Test 2: Request with very short timeout (1 second)")
    try:
        response = client.get(url, proxy_config=proxy_config, timeout=1)
        response.raise_for_status()
        print("   [SUCCESS] Unexpected success")
    except ThordataTimeoutError as e:
        print(f"   [TIMEOUT]  Expected timeout: {e}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    print()

    # Test 3: Invalid URL (will fail)
    print("Test 3: Invalid URL")
    try:
        response = client.get("https://invalid-domain-that-does-not-exist-12345.com", proxy_config=proxy_config, timeout=5)
        response.raise_for_status()
    except ThordataNetworkError as e:
        print(f"    Network error (expected): {e}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    print()

    print("=" * 60)
    print()
    print(" Best Practices:")
    print("   - Always use try-except blocks around proxy requests")
    print("   - Implement retry logic with exponential backoff")
    print("   - Handle Thordata-specific exceptions (ThordataError, ThordataNetworkError, etc.)")
    print("   - Set appropriate timeouts based on your use case")
    print("   - Log errors for debugging and monitoring")


if __name__ == "__main__":
    main()
