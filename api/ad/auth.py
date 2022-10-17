

import requests
from .conf import domain_dict, token_url_dict, host_url_dict


class Auth:

    def __init__(self, client_id, client_secret, redirect_uri, region):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.region = region
        self.domain = domain_dict[self.region]
        self.token_url = token_url_dict[self.region]
        self.host_url = host_url_dict[self.region]
        self.scope = "advertising::campaign_management"
        self.response_type = "code"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        self.uri_path = ""

    def get_grant_url(self):
        return f"{self.host_url}?client_id={self.client_id}&scope={self.scope}&response_type={self.response_type}&redirect_uri={self.redirect_uri}"

    def get_refresh_token(self, code):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(self.token_url, data, headers=self.headers)
        result = response.json()
        # print(f"access_token={result['access_token']}--\n--refresh_token={result['refresh_token']}")
        access_token, refresh_token = result["access_token"], result["refresh_token"]
        return access_token, refresh_token

    def get_new_access_token(self, refresh_token):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(self.token_url, data, headers=self.headers)
        result = response.json()
        access_token = result["access_token"]
        return access_token

