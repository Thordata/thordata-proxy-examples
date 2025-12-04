# 🛰️ Thordata Proxy Examples

Minimal, copy‑pasteable examples showing how to use **Thordata's proxy network**
(Residential / Mobile / Datacenter) from Python and curl.

> For the full SDK, see  
> [thordata-python-sdk](https://github.com/Thordata/thordata-python-sdk).

---

## 🔐 Authentication modes

Thordata proxy gateway supports two common authentication modes:

### 1. Token / username mode (used in most examples)

```text
http://<SCRAPER_TOKEN>:@gate.thordata.com:22225
```

This is convenient when you run from many different machines.
The token is embedded in the proxy URL and authenticated on each request.

### 2. IP whitelist mode (no username/password in the URL)

Add your server's public IP address to the "IP whitelist" section in
the Thordata Dashboard.

Use a plain proxy URL without credentials:

```text
http://gate.thordata.com:22225
```

See `examples/python/ip_whitelist_mode.py` for a complete example
using requests:

```bash
python examples/python/ip_whitelist_mode.py
```

This mode is useful when you don't want to embed secrets in code or
configuration files.

## 🎯 What's in this repo?

- **Python examples**  
  - `examples/python/simple_ip_check.py` – basic IP check via proxy gateway  
  - `examples/python/geo_targeting.py` – illustrate geo‑targeted requests  
  - `examples/python/concurrent_requests.py` – high‑concurrency requests via `AsyncThordataClient`

- **curl example**  
  - `examples/curl/basic_proxy.sh` – quick IP check using curl and the Thordata gateway

---

## ⚙️ Setup

### 1. Clone

```bash
git clone https://github.com/Thordata/thordata-proxy-examples.git
cd thordata-proxy-examples
```

### 2. Create .env

Copy `.env.example` to `.env` and fill in your token from the Thordata Dashboard:

```bash
cp .env.example .env   # Windows: copy .env.example .env
```

### 3. Install dependencies (for Python examples)

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the examples

### 1. Simple IP check (Python)

```bash
python examples/python/simple_ip_check.py
```

You should see a JSON response from `http://httpbin.org/ip` and an origin IP
that belongs to the Thordata proxy network (not your local machine).

### 2. Geo‑targeted request (Python)

```bash
python examples/python/geo_targeting.py
```

Adjust the country variable in the script to test different regions,
depending on your Thordata plan.

### 3. Concurrent requests (Python, async)

```bash
python examples/python/concurrent_requests.py
```

This will send multiple IP check requests in parallel through the proxy network,
using `AsyncThordataClient`.

### 4. Basic curl example

```bash
export THORDATA_SCRAPER_TOKEN=your_token_here
bash examples/curl/basic_proxy.sh
```

---

## 📝 Notes

- These examples focus on proxy usage only. For SERP / Universal / Web Scraper
  APIs, see the SDK and the thordata-cookbook.
- Do not commit your `.env` file or real tokens.

---