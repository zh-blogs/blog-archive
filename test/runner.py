# coding:utf-8
from loguru import logger
import json
import requests
import redis


def runner():
    r = redis.Redis(host='localhost', port=6379, db=0)

    logger.info('start get data from api')
    data = requests.get('https://zhblogs.ohyee.cc/api/blogs?size=-1').json()['data']

    logger.info('insert data to redis')
    r.delete('url_signal_x')
    for i in data:
        if 'feed' in i and i['feed'] != '':
            r.rpush("url_signal_x",
                    json.dumps(str({
                        'name': i['name'],
                        'feed': i['feed']
                    })))

    logger.success('done')
    return True
