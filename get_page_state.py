# coding: utf-8

import redis
import requests
import json

base_url = "https://archive.org/wayback/available?url="


def get_page_state(page_url):
    r = redis.Redis(host='localhost', port=6379, db=2)
    data = r.get(page_url)
    if data is None:
        data = requests.get(base_url + page_url).json()
        if data["archived_snapshots"]:
           r.set(page_url, json.dumps(data), ex=60*60*24)
    else:
        data = json.loads(data)
    return data
