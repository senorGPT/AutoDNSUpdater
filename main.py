from typing import Dict

from bin.log import log, print_seperator, LogType
from bin.dns_record import DNS_Record
from config.config import APIs


def get_current_ip() -> str:
    """
    use requests module to get IPV4 address from ipify API.
    return str representing IPV4 address for current user.
    """
    log(f'Requesting `{APIs["ip"].name}` API for IP', LogType.INFO, end=False)
    api_response = APIs['ip'].get_request()

    if api_response['ip']:
        print(f' : [{LogType.SUCCESS.name}]')
        log(f'Current IP address is {api_response["ip"]}', LogType.INFO)
        return api_response['ip']

    print(f' : [{LogType.ERROR.name}] - Response:\n{api_response}')
    return ""


def does_dns_ip_match_current_ip(dns_record: DNS_Record, current_ip: str) -> bool:
    """
    check if `dns_records` IP matches `current_ip`.
    return True if they do, otherwise return False.
    """
    return dns_record.ip == current_ip


def process_dns_record(dns_record_data: Dict, current_ip: str) -> int:
    """
    process DNS Record data `dns_record_data`. Check if target DNS record ip
    matches `current_ip`.
    return 1 for successful update, 0 for ip match or update failure.
    """
    dns_record = DNS_Record(dns_record_data)

    log(f'DNS Record:  {dns_record}', end=False)
    if does_dns_ip_match_current_ip(dns_record, current_ip):
        print(' - [MATCH]')
        return 0

    dns_record.update_ip(current_ip)
    response = APIs['cloudflare'].put_request(dns_record)

    if response == 200:
        print(' - [UPDATED]')
        return 1
    else:
        print(' - [FAILED TO UPDATE]')
        return 0


def update_dns_records(current_ip):
    """
    request Cloudflare API for all DNS records and ensure each record's ip
    matches `current_ip`.
    """
    api_response = APIs['cloudflare'].get_request()
    dns_records = api_response['result']

    print_seperator()
    if not dns_records:
        log('No Results Found', LogType.ERROR)
        return
    log(f'Cloudflare DNS Results Found : {len(dns_records)}', LogType.INFO)

    dns_records_updated = 0
    for dns_record_data in dns_records:
        dns_records_updated += process_dns_record(dns_record_data, current_ip)

    print_seperator()
    log(f'{dns_records_updated}/{len(dns_records)} DNS Records Updated')


def init():
    """
    init.
    """
    update_dns_records(get_current_ip())


if __name__ == '__main__':
    init()
