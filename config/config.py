from bin.api import API

# Cloudflare API credentials
API_KEY = 'api_key'
API_EMAIL = 'email' # unused as of now
ZONE_ID = 'zone_id'

# API Configurations
APIs = {
    'cloudflare': API(
        'cloudflare',
        f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records',
        {
            'Authorization': f'Bearer {API_KEY.strip()}',
            'Content-Type': 'application/json'
        }, None),

    'ip': API('ipify', 'https://api.ipify.org?format=json')
}
