# coding:utf-8
import redis
import json

r1 = redis.Redis(host='localhost', port=6379, db=1)
r0 = redis.Redis(host='localhost', port=6379, db=0)

def get_site_state(site_host):
    site_state = r1.get(site_host)
    if site_state is None:
        if r0.sismember("work_set", site_host):
            return {"code": 201, "state": "success", "msg": "site is wait for running"}
        else:
            return {"code": 404, "state": "error", "msg": "site not exist"}
    else:
        return {
          "code": 200,
          "state": "success",
          "msg": "site backup work is done",
          "data": json.loads(site_state)
        }
