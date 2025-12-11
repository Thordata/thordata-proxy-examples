#!/usr/bin/env bash
# Sticky session demo - same IP for multiple requests

set -e

: "${THORDATA_USERNAME:?Set THORDATA_USERNAME}"
: "${THORDATA_PASSWORD:?Set THORDATA_PASSWORD}"
: "${THORDATA_PROXY_HOST:=pr.thordata.net}"
: "${THORDATA_PROXY_PORT:=9999}"

SESSION_ID="session-$(date +%s)"
DURATION=10

PROXY_USER="td-customer-${THORDATA_USERNAME}-country-us-sessid-${SESSION_ID}-sesstime-${DURATION}"
PROXY_URL="http://${PROXY_USER}:${THORDATA_PASSWORD}@${THORDATA_PROXY_HOST}:${THORDATA_PROXY_PORT}"

echo "🔒 Sticky Session Test"
echo "   Session ID: ${SESSION_ID}"
echo "   Duration: ${DURATION} minutes"
echo ""

echo "Making 3 requests (should all show same IP):"
for i in 1 2 3; do
    IP=$(curl -s -x "$PROXY_URL" "https://httpbin.org/ip" | jq -r .origin)
    echo "   Request $i: $IP"
done