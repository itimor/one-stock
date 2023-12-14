# -*- coding: utf-8 -*-
# author: itimor
# 云存储api

from hashlib import sha1
import hmac
import requests


class Dogecloud(object):
    def __init__(self, api_path, data):
        self.access_key = 'c815573e569b0686'
        self.secret_key = '827b4a7d28a3e75b28ad6d6748753ad1'
        self.api_url = 'https://api.dogecloud.com'
        self.api_path = api_path
        self.data = data
        self.headers = None
        if self.headers is None:
            self.get_headers()

    def get_headers(self):
        sign_str = self.api_path + "\n" + self.data
        signed_data = hmac.new(self.secret_key.encode('utf-8'), sign_str.encode('utf-8'), sha1)
        sign = signed_data.digest().hex()
        authorization = 'TOKEN ' + self.access_key + ':' + sign
        self.headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
        }

    def request_post(self):
        r = requests.post(self.api_url + self.api_path, data=self.data, headers=self.headers)
        return r.json()

    def request_get(self):
        r = requests.post(self.api_url + self.api_path, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    api_path = '/oss/file/list.json?bucket=itimor'
    data = ""
    dogecloud_api = Dogecloud(api_path, "")
    p = dogecloud_api.request_get()['data']['files']
    print(p)
