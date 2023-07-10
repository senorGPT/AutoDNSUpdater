# AutoDNSUpdater

A simple script that automatically fetches your public IPV4 address and updates DNS records on Cloudflare to ensure they are always synchronized. This repository provides a simple and efficient solution for maintaining up-to-date DNS configurations without manual intervention.

## Features:
* Automatic IP address retrieval: utilizes **configurable** methods to fetch your current public IP address.
* Cloudflare integration: Seamlessly interacts with the Cloudflare API to manage DNS records.
* Dynamic DNS updates: Updates the DNS records on Cloudflare to reflect the latest IP address, ensuring your services are always accessible.
* Configurable settings: Easily customize the script to match your specific DNS zones, Cloudflare account details, and API settings.
* Logging and error handling: Comprehensive logging and error handling mechanisms provide visibility into the execution and help troubleshoot any issues.

## Usage:
1. Set up a Cloudflare account and obtain your API credentials.
2. Configure the script by specifying your Cloudflare credentials and desired DNS records.
3. Run the script, and it will automatically retrieve your IP address and update the DNS records on Cloudflare.

## Images:
![cloudflare_dns_records](https://github.com/senorGPT/Cloudflare_DNS_Record_IP_Updater/assets/4709641/ee66cf51-bb5e-4f42-b766-d27cb213ec44)
![console_output](https://github.com/senorGPT/Cloudflare_DNS_Record_IP_Updater/assets/4709641/55d2b375-8f5e-4f0a-8670-f86dc8349763)

## Requirements: 
1. [Python](https://www.python.org/downloads/)
2. [Python requests Module](https://pypi.org/project/requests/)

## Configuration:
* Edit & Configure `config/config.py`
1. API_KEY : set to Cloudflare Global API Key (found at https://dash.cloudflare.com/profile under `API Tokens` > `Global API Token`)
2. API_EMAIL : the email that is associated with your Cloudflare account
3. ZONE_ID : the zone id for the target webiste (found at Cloudflare Overview website page, click on desired website, on the right side-bar at the bottom will be the `Zone Token`)
4. RECORD_NAME : the respective name for the target DNS Record
5. RECORD_TYPE : the respective type for the target DNS Record

## Run:
`python ./main.py` - within the download path.

## Disclaimer:
Please note that this is a community-driven project and should be used at your own risk. Make sure to review the code and customize it to fit your requirements before deploying it in production environments.
### Contributing:
Contributions are welcome! If you encounter any issues or have ideas for improvements, feel free to submit a pull request or open an issue in the repository.
