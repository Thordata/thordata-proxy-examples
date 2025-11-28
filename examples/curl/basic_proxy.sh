#!/usr/bin/env bash
# Basic example of using Thordata proxy with curl.
#
# Usage:
#   1. Export your token:
#        export THORDATA_SCRAPER_TOKEN=your_token_here
#   2. Run:
#        bash examples/curl/basic_proxy.sh

if [ -z "$THORDATA_SCRAPER_TOKEN" ]; then
  echo "Please set THORDATA_SCRAPER_TOKEN environment variable."
  exit 1
fi

PROXY_HOST="gate.thordata.com"
PROXY_PORT="22225"

TARGET_URL="http://httpbin.org/ip"

echo "Requesting $TARGET_URL via Thordata proxy..."
curl -x "http://$THORDATA_SCRAPER_TOKEN:@$PROXY_HOST:$PROXY_PORT" "$TARGET_URL"
echo