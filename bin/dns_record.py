from typing import Dict


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
