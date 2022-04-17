# coding:utf-8

import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

wait_list = r.lrange("wait_list", 0, -1)

with open('./dist/wait_list.json', 'w', encoding='utf-8') as _f:
    encode_list = [str(i, encoding='utf-8') for i in wait_list]
    print(encode_list)
    _f.write(json.dumps(encode_list, ensure_ascii=False))
