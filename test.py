# coding:utf-8

import redis
import json

conn = redis.Redis('localhost', 6379)

user = {"Name": "Pradeep", "Company": "哈哈SCTL", "Address": "Mumbai", "Location": "RCP"}

conn.set('user', json.dumps(user))

data = json.loads(conn.get('user').decode('utf-8'))

print(data)
