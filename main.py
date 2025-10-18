#!/usr/bin/env python3

from typing import Optional, Dict

from pathlib import Path

from bin.logger import Logger, print_separator, LogType
from bin.dns_record import DNS_Record
from config.config import APIs

DATA = Path('data.txt')


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
