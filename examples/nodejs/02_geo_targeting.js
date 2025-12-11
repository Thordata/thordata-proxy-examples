/**
 * 02 - Geo-Targeted Request
 * 
 * Request from a specific country/region.
 * 
 * Usage: 
 *   node 02_geo_targeting.js
 *   node 02_geo_targeting.js --country de
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

// Parse command line args
const args = process.argv.slice(2);
let country = 'us';
for (let i = 0; i < args.length; i++) {
    if (args[i] === '--country' && args[i + 1]) {
        country = args[i + 1].toLowerCase();
    }
}

if (!USERNAME || !PASSWORD) {
    console.error('❌ Error: Set THORDATA_USERNAME and THORDATA_PASSWORD in .env');
    process.exit(1);
}

async function main() {
    // Build username with geo-targeting
    const geoUsername = `td-customer-${USERNAME}-country-${country}`;
    const proxyUrl = `http://${geoUsername}:${PASSWORD}@${HOST}:${PORT}`;
    const agent = new HttpsProxyAgent(proxyUrl);

    console.log(`🌍 Geo-targeting: ${country.toUpperCase()}`);
    console.log(`   Username: ${geoUsername}\n`);

    const url = 'https://ipinfo.io/json';

    try {
        const response = await axios.get(url, {
            httpAgent: agent,
            httpsAgent: agent,
            timeout: 30000,
        });

        const data = response.data;
        console.log('✅ Response:');
        console.log(`   IP:      ${data.ip}`);
        console.log(`   Country: ${data.country}`);
        console.log(`   Region:  ${data.region}`);
        console.log(`   City:    ${data.city}`);
    } catch (error) {
        console.error(`❌ Error: ${error.message}`);
        process.exit(1);
    }
}

main();