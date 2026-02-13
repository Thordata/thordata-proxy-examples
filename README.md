# 🌐 Thordata Proxy Examples

<div align="center">

**Complete examples for using Thordata's proxy network with the official Python SDK.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](examples/python/)
[![SDK Version](https://img.shields.io/badge/SDK-1.8.4+-green)](https://pypi.org/project/thordata-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[Thordata Dashboard](https://www.thordata.com) • [Python SDK](https://github.com/Thordata/thordata-python-sdk) • [Documentation](https://doc.thordata.com)

</div>

---

## 🎯 What's in this repo?

Copy-paste ready examples showing how to use **Thordata's proxy network** (Residential, Mobile, Datacenter, ISP) with the official Python SDK v1.8.4+.

All examples use modern SDK features including:
- ✅ `ProxyConfig` for flexible proxy configuration
- ✅ `StickySession` for IP persistence
- ✅ Async support with `AsyncThordataClient`
- ✅ Comprehensive error handling
- ✅ Type-safe code with full IDE support

---

## ⚙️ Quick Setup

### 1. Clone the repository

```bash
git clone https://github.com/Thordata/thordata-proxy-examples.git
cd thordata-proxy-examples
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or install from source:

```bash
pip install -e .
```

### 3. Configure credentials

```bash
cp .env.example .env
# Edit .env with your credentials from Thordata Dashboard
```

Required environment variables (see unified `.env.example`):
- `THORDATA_SCRAPER_TOKEN` - Your scraper token (found in Dashboard)
- `THORDATA_RESIDENTIAL_USERNAME` - Your residential proxy username
- `THORDATA_RESIDENTIAL_PASSWORD` - Your residential proxy password

### 4. Run examples

```bash
cd examples/python
python 01_simple_ip_check.py
```

---

## 📖 Examples Overview

| File | Description |
|------|-------------|
| `01_simple_ip_check.py` | Basic IP verification through proxy |
| `02_geo_targeting.py` | Request from specific country/state/city |
| `03_sticky_session.py` | Maintain same IP across requests |
| `04_concurrent_requests.py` | High-concurrency async requests |
| `05_different_products.py` | Compare Residential vs Mobile vs Datacenter vs ISP |
| `06_async_geo_targeting.py` | Async geo-targeting with parallel requests |
| `07_error_handling.py` | Proper error handling patterns |

---

## 🚀 Quick Start Examples (Python)

### Basic Proxy Request

```python
from thordata import ThordataClient, ProxyConfig, ProxyProduct

client = ThordataClient()

proxy = ProxyConfig(
    username="YOUR_RESIDENTIAL_USERNAME",
    password="YOUR_RESIDENTIAL_PASSWORD",
    product=ProxyProduct.RESIDENTIAL,
    country="us",
)

response = client.get("https://ipinfo.io/json", proxy_config=proxy)
print(response.json())
```

### Geo-Targeting

```python
from thordata import ThordataClient, ProxyConfig, ProxyProduct

client = ThordataClient()

proxy = ProxyConfig(
    username="YOUR_RESIDENTIAL_USERNAME",
    password="YOUR_RESIDENTIAL_PASSWORD",
    product=ProxyProduct.RESIDENTIAL,
    country="jp",
    city="tokyo",
)

response = client.get("https://ipinfo.io/json", proxy_config=proxy)
print(response.json())
```

### Sticky Session

```python
from thordata import ThordataClient, StickySession

client = ThordataClient()

session = StickySession(
    username="YOUR_RESIDENTIAL_USERNAME",
    password="YOUR_RESIDENTIAL_PASSWORD",
    country="us",
    duration_minutes=10,
)

response1 = client.get("https://ipinfo.io/json", proxy_config=session)
response2 = client.get("https://ipinfo.io/json", proxy_config=session)
print(response1.json(), response2.json())
```

### Async High-Concurrency (without upstream proxy)

```python
import asyncio
from thordata import AsyncThordataClient


async def main():
    async with AsyncThordataClient() as client:
        tasks = [client.get("https://ipinfo.io/json") for _ in range(10)]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(await r.json())


asyncio.run(main())
```

---

## 📦 Proxy Products & Ports

| Product | Port | Use Case |
|---------|------|----------|
| Residential | 9999 | General scraping, geo-targeting |
| Mobile | 5555 | Mobile-specific content |
| Datacenter | 7777 | High-speed, cost-effective |
| ISP (Static) | 6666 | Long-term sessions |

---

## 🌍 Geo-Targeting Parameters

Use `ProxyConfig` to specify targeting:

```python
ProxyConfig(
    username="your_username",
    password="your_password",
    country="us",           # 2-letter country code
    state="california",     # State name
    city="los_angeles",    # City name
    asn="AS7922",          # ISP ASN (requires country)
)
```

**Examples:**

```python
# United States
ProxyConfig(..., country="us")

# California, USA
ProxyConfig(..., country="us", state="california")

# Los Angeles, California, USA
ProxyConfig(..., country="us", state="california", city="los_angeles")

# Specific ISP (ASN)
ProxyConfig(..., country="us", asn="AS7922")
```

---

## 🔄 Sticky Sessions

Keep the same IP for multiple requests:

```python
from thordata import StickySession

session = StickySession(
    username="your_username",
    password="your_password",
    country="us",
    duration_minutes=10  # 1-90 minutes
)

# All requests using this session will use the same IP
client.get(url1, proxy_config=session)
client.get(url2, proxy_config=session)
```

---

## 🔐 Authentication Modes

Thordata supports two authentication modes:

### 1. Username/Password Mode (Recommended)

Credentials are embedded in the proxy URL via `ProxyConfig`:

```python
proxy = ProxyConfig(
    username="your_username",
    password="your_password",
    country="us"
)
```

### 2. IP Whitelist Mode

Add your server's IP to the Dashboard whitelist, then use proxy without credentials (not shown in examples, but supported by SDK).

---

## ⚠️ Important Notes

- **Don't commit credentials** - Keep `.env` in `.gitignore`
- **Respect rate limits** - Check your plan's concurrency limits
- **Use appropriate product** - Residential for sensitive sites, Datacenter for speed
- **Handle errors** - Implement retry logic for transient failures
- **Environment variables** - SDK automatically reads from environment or use `load_env_file()`
- **Upstream proxy** - When using an upstream proxy (e.g. Clash), prefer the sync `ThordataClient`
  for Proxy Network requests, or follow the SDK's guidance for `AsyncThordataClient` limitations with
  HTTPS upstream proxies.

---

## 🧪 Testing

Run all examples to verify your setup:

```bash
cd examples/python
for file in *.py; do
    echo "Running $file..."
    python "$file" || echo "Failed: $file"
done
```

---

## 🔗 Related Resources

- **[Thordata Python SDK](https://github.com/Thordata/thordata-python-sdk)** - Full-featured Python client
- **[Thordata MCP Server](https://github.com/Thordata/thordata-mcp-server)** - MCP server for AI agents
- **[Documentation](https://doc.thordata.com)** - Complete API reference

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Ready to get started?** 🚀

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python examples/python/01_simple_ip_check.py
```
