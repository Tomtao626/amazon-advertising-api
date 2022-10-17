import time

import requests
from .conf import domain_dict
import json


class ProClient(object):
    """
    proficient
    """
    def __init__(self, access_token, region, client_id):
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Amazon-Advertising-API-ClientId": client_id
        }
        self.domain = domain_dict[region]
        self.method = "get"
        self.data = None
        self.uri_path = None

    def execute(self):
        url = self.domain + self.uri_path
        print("request time   --- ", time.strftime("strat... %Y-%m-%d %H:%M:%S", time.localtime()))
        print("request url    --- ", url)
        print("request header --- ", self.headers)
        if self.method == "delete":
            response = requests.delete(url, headers=self.headers).text
            return response
        if self.data:
            self.data = json.dumps(self.data)
        response = requests.request(self.method, url, headers=self.headers, data=self.data).json()
        print("response --- ", json.dumps(response))
        return response

    def execute_download(self, url):
        s = requests.Session()
        self.headers.pop("Content-Type")
        self.headers["Accept-encoding"] = "gzip"
        response = s.get(url, headers=self.headers)
        return ((response.__dict__)['url'])


class Client(ProClient):
    def __init__(self, access_token, profile_id, region, client_id):
        self.profile_id = profile_id
        super(Client, self).__init__(access_token, region, client_id)
        self.headers["Amazon-Advertising-API-Scope"] = self.profile_id





