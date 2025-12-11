# Python Proxy Examples

Examples using the official [Thordata Python SDK](https://github.com/Thordata/thordata-python-sdk).

---

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp ../../.env.example ../../.env
# Edit .env with your credentials
```

---

## Examples

| # | File | Description |
|---|------|-------------|
| 1 | `01_simple_ip_check.py` | Basic IP check through proxy |
| 2 | `02_geo_targeting.py` | Request from specific location |
| 3 | `03_sticky_session.py` | Same IP across multiple requests |
| 4 | `04_concurrent_requests.py` | Async high-concurrency |
| 5 | `05_different_products.py` | Residential vs Mobile vs DC |
| 6 | `06_ip_whitelist_mode.py` | IP whitelist authentication |
| 7 | `07_error_handling.py` | Proper error handling |

---

## Run

```bash
python 01_simple_ip_check.py
python 02_geo_targeting.py --country us --city seattle
python 03_sticky_session.py --duration 10
```