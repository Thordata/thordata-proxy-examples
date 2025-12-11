#!/usr/bin/env bash
# Basic proxy test

set -e

: "${THORDATA_USERNAME:?Set THORDATA_USERNAME}"
: "${THORDATA_PASSWORD:?Set THORDATA_PASSWORD}"
: "${THORDATA_PROXY_HOST:=pr.thordata.net}"
: "${THORDATA_PROXY_PORT:=9999}"

PROXY_USER="td-customer-${THORDATA_USERNAME}"
PROXY_URL="http://${PROXY_USER}:${THORDATA_PASSWORD}@${THORDATA_PROXY_HOST}:${THORDATA_PROXY_PORT}"

echo "🌐 Basic Proxy Test"
echo "   Proxy: ${THORDATA_PROXY_HOST}:${THORDATA_PROXY_PORT}"
echo ""

curl -s -x "$PROXY_URL" "https://httpbin.org/ip" | jq .