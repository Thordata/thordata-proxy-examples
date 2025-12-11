/**
 * 03 - Concurrent Requests
 * 
 * Send multiple requests in parallel.
 * 
 * Usage: node 03_concurrent_requests.js
 */

import axios from 'axios';
import { HttpsProxyAgent } from 'https-proxy-agent';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: join(__dirname, '../../.env') });

const USERNAME = process.env.THORDATA_USERNAME;
const PASSWORD = process.env.THORDATA_PASSWORD;
const HOST = process.env.THORDATA_PROXY_HOST || 'pr.thordata.net';
const PORT = process.env.THORDATA_PROXY_PORT || '9999';

const REQUEST_COUNT = 10;

if (!USERNAME || !PASSWORD) {
    console.error('❌ Error: Set THORDATA_USERNAME and THORDATA_PASSWORD in .env');
    process.exit(1);
}

async function fetchIp(agent, id) {
    try {
        const response = await axios.get('https://httpbin.org/ip', {
            httpAgent: agent,
            httpsAgent: agent,
            timeout: 30000,
        });
        return { id, ip: response.data.origin, status: 'success' };
    } catch (error) {
        return { id, ip: null, status: `error: ${error.message}` };
    }
}

async function main() {
    const proxyUrl = `http://td-customer-${USERNAME}:${PASSWORD}@${HOST}:${PORT}`;
    const agent = new HttpsProxyAgent(proxyUrl);

    console.log(`🚀 Sending ${REQUEST_COUNT} concurrent requests...\n`);

    const startTime = Date.now();

    // Create all promises
    const promises = Array.from({ length: REQUEST_COUNT }, (_, i) =>
        fetchIp(agent, i + 1)
    );

    // Execute all concurrently
    const results = await Promise.all(promises);

    const elapsed = (Date.now() - startTime) / 1000;

    // Display results
    const uniqueIps = new Set();
    let successCount = 0;

    for (const result of results) {
        const icon = result.status === 'success' ? '✅' : '❌';
        console.log(`   ${icon} Request ${result.id}: ${result.ip || result.status}`);
        if (result.status === 'success') {
            successCount++;
            uniqueIps.add(result.ip);
        }
    }

    console.log('\n📊 Summary:');
    console.log(`   Total requests:  ${REQUEST_COUNT}`);
    console.log(`   Successful:      ${successCount}`);
    console.log(`   Unique IPs:      ${uniqueIps.size}`);
    console.log(`   Total time:      ${elapsed.toFixed(2)}s`);
    console.log(`   Requests/second: ${(REQUEST_COUNT / elapsed).toFixed(1)}`);
}

main();