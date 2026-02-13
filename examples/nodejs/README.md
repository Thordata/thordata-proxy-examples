# Node.js Proxy Examples

Examples using axios with Thordata proxy network.

---

## Setup

```bash
npm install

# Configure credentials
cp ../../.env.example ../../.env
# Edit .env with your credentials (THORDATA_SCRAPER_TOKEN, THORDATA_RESIDENTIAL_USERNAME, THORDATA_RESIDENTIAL_PASSWORD)
```

---

## Run

```bash
node 01_simple_ip_check.js
node 02_geo_targeting.js
node 03_concurrent_requests.js
```