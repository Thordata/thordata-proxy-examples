#!/usr/bin/env python3
"""
Quick test script to validate all examples.

Usage:
    python test_examples.py
"""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env
load_dotenv()

EXAMPLES_DIR = Path(__file__).parent / "examples" / "python"


def check_env():
    """Check if required environment variables are set."""
    required = [
        "THORDATA_SCRAPER_TOKEN",
        "THORDATA_RESIDENTIAL_USERNAME",
        "THORDATA_RESIDENTIAL_PASSWORD",
    ]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        print("Missing required environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\nPlease set these in your .env file.")
        return False
    return True


def test_example(script_path: Path) -> tuple[bool, str]:
    """Test a single example script."""
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=script_path.parent,
        )
        if result.returncode == 0:
            return True, "OK"
        else:
            return False, result.stderr[:200] if result.stderr else "Unknown error"
    except subprocess.TimeoutExpired:
        return False, "Timeout (>60s)"
    except Exception as e:
        return False, str(e)[:200]


def main():
    print("Testing Thordata Proxy Examples")
    print("=" * 60)
    print()

    if not check_env():
        sys.exit(1)

    # Find all Python example files
    example_files = sorted(EXAMPLES_DIR.glob("*.py"))
    example_files = [f for f in example_files if f.name != "__init__.py"]

    if not example_files:
        print("No example files found!")
        sys.exit(1)

    print(f"Found {len(example_files)} example(s) to test:")
    print()

    results = []
    for example_file in example_files:
        print(f"Testing {example_file.name}...", end=" ")
        success, message = test_example(example_file)
        status = "[OK]" if success else "[FAIL]"
        print(f"{status}")
        if not success:
            print(f"   Error: {message}")
        results.append((example_file.name, success))

    print()
    print("=" * 60)
    print("Summary:")
    print()

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "[OK]" if success else "[FAIL]"
        print(f"   {status} {name}")

    print()
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("All tests passed!")
        return 0
    else:
        print(f"{total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
