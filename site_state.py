# coding:utf-8

import redis
import json

r1 = redis.Redis(host='localhost', port=6379, db=1)
r0 = redis.Redis(host='localhost', port=6379, db=0)


def get_site_state(site_host):
    site_state = r1.get(site_host)
    if site_state is None:
        if r0.sismember("work_set", site_host):
            return {"state": "SUCCESS", "msg": "site is wait for  running", "code": 201}
        else:
            return {"state": "error", "msg": "site not exist", "code": 404}
    else:
        return {"state": "SUCCESS", "msg": "site backup work is done", "code": 200, "data": json.loads(site_state)}
