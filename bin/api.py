import requests
from typing import Dict

from bin.dns_record import DNS_Record


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
