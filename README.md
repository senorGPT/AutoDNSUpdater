# Cloudflare_DNS_Record_IP_Updater

![cloudflare_dns_records](https://github.com/senorGPT/Cloudflare_DNS_Record_IP_Updater/assets/4709641/ee66cf51-bb5e-4f42-b766-d27cb213ec44)
![console_output](https://github.com/senorGPT/Cloudflare_DNS_Record_IP_Updater/assets/4709641/55d2b375-8f5e-4f0a-8670-f86dc8349763)

## Requirements: 
1. [Python](https://www.python.org/downloads/)
2. [Python requests Module](https://pypi.org/project/requests/)

## Setup:
1. Edit & Configure `config/config.py`
2. API_KEY : set to Cloudflare Global API Key (found at https://dash.cloudflare.com/profile under `API Tokens` > `Global API Token`)
3. API_EMAIL : the email that is associated with your Cloudflare account
4. ZONE_ID : the zone id for the target webiste (found at Cloudflare Overview website page, click on desired website, on the right side-bar at the bottom will be the `Zone Token`)
5. RECORD_NAME : the respective name for the target DNS Record
6. RECORD_TYPE : the respective type for the target DNS Record

## Run:
`python ./main.py` - within the download path.
