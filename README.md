# Thordata Proxy Examples

Copy-paste examples for using Thordata proxy infrastructure and web data APIs.

Examples cover:

- Residential proxies
- Mobile proxies
- Static ISP proxies
- Datacenter proxies
- SERP API
- Web Unlocker
- Web Scraper API
- Geo-targeting
- Sticky sessions
- Concurrent requests
- Error handling

## Quick Links

- [Start with Thordata](https://www.thordata.com/?ls=github&lk=thordata)
- [Open Dashboard](https://dashboard.thordata.com)
- [Documentation](https://doc.thordata.com)
- [Python SDK](https://github.com/Thordata/thordata-python-sdk)
- [Proxy Products](https://www.thordata.com/products/residential-proxies)
- [Static ISP Proxies](https://www.thordata.com/products/isp-proxies)
- [SERP API](https://www.thordata.com/products/serp-api)
- [Web Scraper API](https://www.thordata.com/products/web-scraper-api)
- [Web Unlocker](https://www.thordata.com/products/web-unlocker)
- [Scraping Browser](https://www.thordata.com/products/scraping-browser)

## Quick Setup

Clone the repository:

```bash
git clone https://github.com/Thordata/thordata-proxy-examples.git
cd thordata-proxy-examples
```

Install the Python SDK:

```bash
pip install thordata-sdk
```

For Python examples:

```bash
cp .env.example .env
```

Set your credentials in `.env`:

```bash
THORDATA_SCRAPER_TOKEN=your_scraper_token
THORDATA_RESIDENTIAL_USERNAME=your_username
THORDATA_RESIDENTIAL_PASSWORD=your_residential_password
```

Never commit `.env` or real credentials.

## Examples By Language

| Language | Location |
| --- | --- |
| Python | `examples/python/` |
| Node.js | `examples/nodejs/` |
| Go | `examples/go/` |
| Java | `examples/java/` |
| curl | `examples/curl/` |

## Examples By Use Case

| Use case | Examples |
| --- | --- |
| Basic proxy request | `examples/python/01_simple_ip_check.py` |
| Geo-targeting | `examples/python/02_geo_targeting.py` |
| Sticky session | `examples/python/03_sticky_session.py` |
| Concurrent requests | `examples/python/04_concurrent_requests.py` |
| Product comparison | `examples/python/05_different_products.py` |
| Async geo-targeting | `examples/python/06_async_geo_targeting.py` |
| Error handling | `examples/python/07_error_handling.py` |
| curl proxy usage | `examples/curl/` |
| Go proxy usage | `examples/go/` |
| Node.js proxy usage | `examples/nodejs/` |
| Java proxy usage | `examples/java/` |

## Proxy Products

| Product | Typical use |
| --- | --- |
| Residential Proxies | Localized access and sensitive web scraping |
| Mobile Proxies | Mobile-network and carrier-specific workflows |
| Static ISP Proxies | Stable identity and long sessions |
| Datacenter Proxies | High-speed and high-volume requests |

Review the product documentation for current availability, pricing, limits,
and supported targeting options.

## Web Data APIs

Use the examples and official documentation for:

- [SERP API](https://www.thordata.com/products/serp-api)
- [Web Scraper API](https://www.thordata.com/products/web-scraper-api)
- [Web Unlocker](https://www.thordata.com/products/web-unlocker)
- [Scraping Browser](https://www.thordata.com/products/scraping-browser)

## Environment Variables

The examples use environment variables for credentials.

Common variables include:

```bash
THORDATA_SCRAPER_TOKEN=your_scraper_token
THORDATA_PUBLIC_TOKEN=your_public_token
THORDATA_PUBLIC_KEY=your_public_key
THORDATA_RESIDENTIAL_USERNAME=your_residential_username
THORDATA_RESIDENTIAL_PASSWORD=your_residential_password
```

Only set the variables required by the example you are running. Do not place
real credentials directly in source files.

## Running Examples

Python:

```bash
cd examples/python
python 01_simple_ip_check.py
```

curl:

```bash
bash examples/curl/01_basic_proxy.sh
```

Go:

```bash
cd examples/go
go run ./simple_ip_check
```

Node.js:

```bash
cd examples/nodejs
node 01_simple_ip_check.js
```

Java:

```bash
cd examples/java
javac SimpleIpCheck.java
java SimpleIpCheck
```

Some examples require product-specific credentials or account permissions.
Check the example comments and the official documentation before running them.

## Safety And Usage

Use these examples only for lawful and authorized web data workflows.

- Respect website terms and access restrictions.
- Do not commit API tokens, usernames, or passwords.
- Do not use the examples to bypass access controls.
- Follow applicable privacy and data protection requirements.
- Respect rate limits and your account plan.
- Review the applicable product terms before collecting or redistributing data.

## Related Resources

- [Thordata Python SDK](https://github.com/Thordata/thordata-python-sdk)
- [Thordata MCP](https://github.com/Thordata/thordata-mcp)
- [Thordata LangChain Tools](https://github.com/Thordata/thordata-langchain-tools)
- [Thordata n8n Integration](https://github.com/Thordata/n8n-nodes-thordata)
- [Thordata Cookbook](https://github.com/Thordata/thordata-cookbook)
- [Thordata Organization](https://github.com/Thordata)

## Support

For technical questions, open an issue in this repository.

For account, product, licensing, or commercial questions, contact the
[Thordata team](https://www.thordata.com/contact-us).

## License

MIT License. See [LICENSE](LICENSE).
