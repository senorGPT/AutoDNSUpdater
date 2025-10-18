#!/usr/bin/env python3

import datetime
import requests
from enum import Enum
from pathlib import Path
from typing import Optional, Dict

DATA = Path('data.txt')
SEPARATOR_LENGTH = 60


# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
class DNS_Record():
    def __init__(self, data: Dict = None):
        self.id = data['id']
        self.name = data['name']
        self.ip = data['content']

        self.json = data


    def __str__(self):
        return f'Name: {self.name:<30} |  \tIP: {self.ip:<30}'


    def update_ip(self, new_ip: str):
        """
        update the current DNS_Record's ip attribute to `new_ip`.
        """
        self.ip = new_ip
        self.json['content'] = self.ip


# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
class API:
    def __init__(self, name: str = None, url: str = None, headers: Dict = None, params: Dict = None) -> None:
        self.name = name
        self.url = url
        self.headers = headers
        self.params = params

        self.response = None


    def __str__(self) -> str:
        return f'{self.name}: {self.url}'


    def get_request(self) -> Dict:
        """
        submit a get request for `self.url`.
        returns the response as a json object.
        """
        self.response = requests.get(
            self.url, headers=self.headers, params=self.params)
        return self.response.json()


    def put_request(self, dns_record: DNS_Record) -> int:
        """
        submit a put request for `self.url` updating the dns record.
        returns the response status code.
        """
        response = requests.put(
            f'{self.url}/{dns_record.id}', headers=self.headers, json=dns_record.json)
        return response.status_code


# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
class LogType(Enum):
    INFO = 1
    SUCCESS = 2
    WARN = 3
    ERROR = 4


class Logger():
    def __init__(self):
        self.file = open('auto_dns_updater.log', 'a')


    def __del__(self):
        self.file.close()


    def get_datetime_stamp(self) -> str:
        """
        return the current date and time in desired format as a str.
        """
        current_time = datetime.datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S")


    def close(self) -> None:
        """
        close the opened file for reading.
        """
        self.file.close()


    def write_to_file(self, message: str) -> None:
        """
        write to file `message`.
        """
        self.file.write(f'[{self.get_datetime_stamp()}]: {message}')


    def log(self, message: str, target_log_type: LogType = LogType.INFO, end: bool = True, prefix: bool = False) -> None:
        """
        output to console `message` with prefix of `target_log_type` name wrapped in square brackets and equally spaced.
        """
        prefix = ""
        if prefix:
            message_type = target_log_type.name
            for log_type in LogType:
                if log_type.value == target_log_type.value:
                    message_type = log_type.name
                    break
            prefix = f' [{message_type}]{(10 - len(message_type)) * " "}- '

        final_message = f'{prefix}{message}'
        if end:
            print(f'{final_message}')
            self.write_to_file(f'{final_message}\n')
        else:
            print(f'{final_message}', end='')
            self.write_to_file(f'{final_message}')


def print_separator(separator_length: int = SEPARATOR_LENGTH) -> None:
    """
    print a standard separator, with a desired length of `separator_length`.
    """
    print(f'{"-" * separator_length}')


# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---

# Cloudflare API credentials
API_KEY = ''
API_EMAIL = '' # unused as of now
ZONE_ID = ''

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

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # ---


def read_ip_from_file() -> str:
    """
    Read the current IP address from the DATA file if it exists.
    """

    return DATA.read_text(encoding='utf-8').strip()


def write_ip_to_file(ip: str) -> None:
    """
    Overwrite the DATA file with the given IP address.
    """
    DATA.write_text(ip, encoding='utf-8')


def get_saved_ip(logger: Logger) -> Optional[str]:
    """
    Get the saved IP (if present).
    """
    if not DATA.exists():
        return None

    saved_ip = read_ip_from_file()
    logger.log(f'Found IP saved data file & data - {saved_ip}')
    return saved_ip


def get_current_ip(logger: Logger) -> str:
    """
    use requests module to get IPV4 address from ipify API.
    return str representing IPV4 address for current user.
    """
    logger.log(f'Requesting `{APIs["ip"].name}` API for IP', LogType.INFO, end=False)
    api_response = APIs['ip'].get_request()

    if api_response['ip']:
        logger.log(f' : [{LogType.SUCCESS.name}]', None, prefix=False)
        logger.log(f'Current IP address is {api_response["ip"]}', LogType.INFO)
        return api_response['ip']

    logger.log(f' : [{LogType.ERROR.name}] - Response:\n{api_response}', None, prefix=False)
    return ""


def does_dns_ip_match_current_ip(dns_record: DNS_Record, current_ip: str) -> bool:
    """
    check if `dns_records` IP matches `current_ip`.
    return True if they do, otherwise return False.
    """
    return dns_record.ip == current_ip


def process_dns_record(dns_record_data: Dict, current_ip: str, logger: Logger) -> int:
    """
    process DNS Record data `dns_record_data`. Check if target DNS record ip
    matches `current_ip`.
    return 1 for successful update, 0 for ip match or update failure.
    """
    dns_record = DNS_Record(dns_record_data)

    logger.log(f'DNS Record:  {dns_record}', end=False)
    if does_dns_ip_match_current_ip(dns_record, current_ip):
        logger.log(' - [MATCH]', None, prefix=False)
        return 0

    dns_record.update_ip(current_ip)
    response = APIs['cloudflare'].put_request(dns_record)

    if response == 200:
        logger.log(' - [UPDATED]', None, prefix=False)
        return 1
    else:
        logger.log(' - [FAILED TO UPDATE]', None, prefix=False)
        return 0


def update_dns_records(current_ip: str, logger: Logger):
    """
    request Cloudflare API for all DNS records and ensure each record's ip
    matches `current_ip`.
    """
    api_response = APIs['cloudflare'].get_request()
    # check if we got a bad response from cloudflare
    if api_response is None or api_response['result'] is None:
        logger.log(f'Bad api response from cloudflare: {api_response.get("result")}')
        return

    dns_records = api_response['result']

    print_separator()
    if not dns_records:
        logger.log('No Results Found', LogType.ERROR)
        return
    logger.log(f'Cloudflare DNS Records Found : {len(dns_records)}', LogType.INFO)

    dns_records_updated = 0
    for dns_record_data in dns_records:
        dns_records_updated += process_dns_record(dns_record_data, current_ip, logger)

    print_separator()
    logger.log(f'{dns_records_updated}/{len(dns_records)} DNS Records Updated to new IP {current_ip}')


def init():
    """
    init.
    """
    logger = Logger()

    saved_ip    = get_saved_ip(logger)
    current_ip  = get_current_ip(logger)
    # check if the saved ip matches the current ip
    if saved_ip == current_ip:
        logger.log(f'Saved IP ({saved_ip}) matches current IP ({current_ip}) - Skipping CloudFlare Requests')
        return

    update_dns_records(current_ip, logger)

    logger.log(f'Saved IP to data.txt - {current_ip}')
    write_ip_to_file(current_ip)


if __name__ == '__main__':
    init()
