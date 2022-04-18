# coding:utf-8

import redis

r1 = redis.Redis(host='localhost', port=6379, db=1)
r0 = redis.Redis(host='localhost', port=6379, db=0)


def get_runner_state():
    """
    获取所有的runner的状态
    :return:
    """
    suc_runner_state = r1.keys()
    all_runner_state = r0.smembers("work_set")
    work_list = r0.lrange("work_list", 0 , -1)
    return {
        "message": "success",
        "code": 200,
        "data": {
            "suc_runner_state": suc_runner_state,
            "all_runner_state": all_runner_state,
            "work_list": work_list
        }
    }
