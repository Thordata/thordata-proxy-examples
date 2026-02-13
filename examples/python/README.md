# Python Examples

Complete examples for using Thordata's proxy network with the official Python SDK.

## Prerequisites

- Python 3.9 or higher
- Thordata account with proxy credentials
- `.env` file configured (see root `.env.example`)

## Examples

### 01_simple_ip_check.py
Basic IP verification through proxy. The simplest example to get started.

```bash
python 01_simple_ip_check.py
```

### 02_geo_targeting.py
Request from specific country/state/city using `ProxyConfig`.

```bash
python 02_geo_targeting.py
python 02_geo_targeting.py --country de
python 02_geo_targeting.py --country us --state california --city seattle
```

### 03_sticky_session.py
Maintain same IP across multiple requests using `StickySession`.

```bash
python 03_sticky_session.py
python 03_sticky_session.py --duration 15 --requests 5
```

### 04_concurrent_requests.py
High-concurrency async requests using `AsyncThordataClient`.

```bash
python 04_concurrent_requests.py
python 04_concurrent_requests.py --count 20
```

### 05_different_products.py
Compare different proxy products (Residential, Mobile, Datacenter, ISP).

```bash
python 05_different_products.py
```

### 06_async_geo_targeting.py
Async geo-targeting with parallel requests to multiple countries.

```bash
python 06_async_geo_targeting.py
```

### 07_error_handling.py
Proper error handling patterns with retry logic.

```bash
python 07_error_handling.py
```

## Running All Examples

```bash
for file in *.py; do
    echo "Running $file..."
    python "$file" || echo "Failed: $file"
done
```
