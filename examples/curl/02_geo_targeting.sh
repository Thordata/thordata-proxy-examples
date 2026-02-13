#!/usr/bin/env bash
# Geo-targeted request
#
# Usage: bash 02_geo_targeting.sh [country]

set -e

COUNTRY="${1:-us}"

: "${THORDATA_RESIDENTIAL_USERNAME:?Set THORDATA_RESIDENTIAL_USERNAME}"
: "${THORDATA_RESIDENTIAL_PASSWORD:?Set THORDATA_RESIDENTIAL_PASSWORD}"
: "${THORDATA_PROXY_HOST:=pr.thordata.net}"
: "${THORDATA_PROXY_PORT:=9999}"

PROXY_USER="td-customer-${THORDATA_RESIDENTIAL_USERNAME}-country-${COUNTRY}"
PROXY_URL="http://${PROXY_USER}:${THORDATA_RESIDENTIAL_PASSWORD}@${THORDATA_PROXY_HOST}:${THORDATA_PROXY_PORT}"

echo "🌍 Geo-Targeted Request"
echo "   Country: ${COUNTRY}"
echo "   Username: ${PROXY_USER}"
echo ""

curl -s -x "$PROXY_URL" "https://ipinfo.io/json" | jq .