# 🌐 Thordata Proxy Examples

<div align="center">

**Complete examples for using Thordata's proxy network across multiple languages.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](examples/python/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green?logo=node.js&logoColor=white)](examples/nodejs/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?logo=go&logoColor=white)](examples/go/)
[![curl](https://img.shields.io/badge/curl-grey?logo=curl&logoColor=white)](examples/curl/)

[Thordata Dashboard](https://www.thordata.com) • [Python SDK](https://github.com/Thordata/thordata-python-sdk) • [Documentation](https://doc.thordata.com)

</div>

---

## 🎯 What's in this repo?

Copy-paste ready examples showing how to use **Thordata's proxy network** (Residential, Mobile, Datacenter, ISP) from multiple programming languages.

| Language | Examples | Description |
|----------|----------|-------------|
| [Python](examples/python/) | 7 examples | Using official SDK with ProxyConfig, async, error handling |
| [Node.js](examples/nodejs/) | 3 examples | Using axios with proxy configuration |
| [Go](examples/go/) | 2 examples | Using net/http with proxy |
| [curl](examples/curl/) | 3 examples | Quick command-line testing |

---

## 🔐 Authentication Modes

Thordata supports two authentication modes:

### 1. Username/Password Mode (Recommended)

Credentials are embedded in the proxy URL:

```
http://td-customer-{USERNAME}-country-{COUNTRY}:{PASSWORD}@{HOST}:{PORT}
```

**Example:**

```bash
curl -x "http://td-customer-myuser-country-us:mypassword@pr.thordata.net:9999" "https://httpbin.org/ip"
```

### 2. IP Whitelist Mode

Add your server's IP to the Dashboard whitelist, then use proxy without credentials:

```bash
curl -x "http://pr.thordata.net:9999" "https://httpbin.org/ip"
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

## ⚙️ Quick Setup

### 1. Clone the repository

```bash
git clone https://github.com/Thordata/thordata-proxy-examples.git
cd thordata-proxy-examples
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env with your credentials from Thordata Dashboard
```

### 3. Run examples

Choose your language:

```bash
# Python
cd examples/python
pip install -r requirements.txt
python 01_simple_ip_check.py

# Node.js
cd examples/nodejs
npm install
node 01_simple_ip_check.js

# Go
cd examples/go
go run simple_ip_check.go

# curl
cd examples/curl
export THORDATA_USERNAME=your_username
export THORDATA_PASSWORD=your_password
bash 01_basic_proxy.sh
```

---

## 📖 Examples Overview

### Python Examples

| File | Description |
|------|-------------|
| `01_simple_ip_check.py` | Basic IP verification through proxy |
| `02_geo_targeting.py` | Request from specific country/state/city |
| `03_sticky_session.py` | Maintain same IP across requests |
| `04_concurrent_requests.py` | High-concurrency async requests |
| `05_different_products.py` | Residential vs Mobile vs Datacenter |
| `06_ip_whitelist_mode.py` | Using IP whitelist authentication |
| `07_error_handling.py` | Proper error handling patterns |

### Node.js Examples

| File | Description |
|------|-------------|
| `01_simple_ip_check.js` | Basic proxy request with axios |
| `02_geo_targeting.js` | Geo-targeted requests |
| `03_concurrent_requests.js` | Parallel requests with Promise.all |

### Go Examples

| File | Description |
|------|-------------|
| `simple_ip_check.go` | Basic proxy request |
| `geo_targeting.go` | Geo-targeted requests |

### curl Examples

| File | Description |
|------|-------------|
| `01_basic_proxy.sh` | Simple proxy test |
| `02_geo_targeting.sh` | Country/city targeting |
| `03_sticky_session.sh` | Session persistence |

---

## 🌍 Geo-Targeting Parameters

Embed targeting in the username:

```
td-customer-{USERNAME}[-continent-{CODE}][-country-{CODE}][-state-{NAME}][-city-{NAME}][-asn-{CODE}]
```

**Examples:**

```bash
# United States
td-customer-myuser-country-us

# California, USA
td-customer-myuser-country-us-state-california

# Los Angeles, California, USA
td-customer-myuser-country-us-state-california-city-los_angeles

# Specific ISP (ASN)
td-customer-myuser-country-us-asn-AS7922
```

---

## 🔄 Sticky Sessions

Keep the same IP for multiple requests:

```
td-customer-{USERNAME}-sessid-{SESSION_ID}-sesstime-{MINUTES}
```

**Example:**

```bash
# Same IP for 10 minutes
td-customer-myuser-country-us-sessid-abc123-sesstime-10
```

---

## ⚠️ Important Notes

- Don't commit credentials - Keep `.env` in `.gitignore`
- Respect rate limits - Check your plan's concurrency limits
- Use appropriate product - Residential for sensitive sites, Datacenter for speed
- Handle errors - Implement retry logic for transient failures

---

## 🔗 Related Resources

- **[Thordata Python SDK](https://github.com/Thordata/thordata-python-sdk)** - Full-featured Python client
- **[Thordata Cookbook](https://github.com/Thordata/thordata-cookbook)** - AI/LLM integration examples
- **[Documentation](https://doc.thordata.com)** - Complete API reference

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.