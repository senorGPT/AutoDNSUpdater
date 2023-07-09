from bin.api import API

# Cloudflare API credentials
API_KEY = 'api_key'
API_EMAIL = 'email'
ZONE_ID = 'zone_id'

RECORD_NAME = 'yourwebsite.com'
RECORD_TYPE = 'A'

# API Configurations
APIs = {
    'cloudflare': API(
        'cloudflare',
        f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records',
        {
            'X-Auth-Email': API_EMAIL,
            'X-Auth-Key': API_KEY,
            'Content-Type': 'application/json'
        }, None),

    'ip': API('ipify', 'https://api.ipify.org?format=json')
}
