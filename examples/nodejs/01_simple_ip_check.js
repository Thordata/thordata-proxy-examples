/**
 * 01 - Simple IP Check via Thordata Proxy
 * 
 * Basic example: verify your request goes through the proxy.
 * 
 * Usage: node 01_simple_ip_check.js
 */

import axios from 'axios';
import { HttpsProxyAgent } from 'https-proxy-agent';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

// Load .env from repo root
const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: join(__dirname, '../../.env') });

const USERNAME = process.env.THORDATA_RESIDENTIAL_USERNAME;
const PASSWORD = process.env.THORDATA_RESIDENTIAL_PASSWORD;
const HOST = process.env.THORDATA_PROXY_HOST || 'pr.thordata.net';
const PORT = process.env.THORDATA_PROXY_PORT || '9999';

if (!USERNAME || !PASSWORD) {
    console.error('[ERROR] Set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in .env');
    process.exit(1);
}

async function main() {
    // Build proxy URL
    const proxyUrl = `http://td-customer-${USERNAME}:${PASSWORD}@${HOST}:${PORT}`;
    const agent = new HttpsProxyAgent(proxyUrl);

    const url = 'https://httpbin.org/ip';

    console.log(`🌐 Requesting: ${url}`);
    console.log('   via Thordata proxy network...\n');

    try {
        const response = await axios.get(url, {
            httpAgent: agent,
            httpsAgent: agent,
            timeout: 30000,
        });

        console.log('✅ Success!');
        console.log(`   Your proxy IP: ${response.data.origin}`);
    } catch (error) {
        console.error(`❌ Error: ${error.message}`);
        process.exit(1);
    }
}

main();