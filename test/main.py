# coding: utf-8
from concurrent.futures import ThreadPoolExecutor, as_completed
from runner import runner

import sys

sys.path.append('../')
from loguru import logger
import redis
import json
import os
from urllib.parse import urlparse

from feed_url_to_list import feed_url_to_list
from post_url_to_archive import post_url_to_archive


def exec(data):
    arr = eval(json.loads(data))

    name = arr['name']
    feed = arr['feed']

    logger.success('start process > ' + name)
    feed_list = feed_url_to_list(feed)
    succ = [];
    fail = [];

    if 'data' in feed_list:
        for j in feed_list["data"]:
            link_url = j["link"]
            link_title = j["title"]
            if post_url_to_archive(link_url):
                # success
                logger.success("{} {}".format(link_title, link_url))
                succ.append(link_url)
            else:
                # failed
                logger.error("{} {}".format(link_title, link_url))
                fail.append(link_url)
    else:
        logger.error('{} feed 解析失败'.format(name))

    # create temp
    with open(os.getcwd() + '/data/{}.json'.format(urlparse(feed).netloc), mode='w', encoding='utf-8') as f:
        d = json.dumps({
            "link": feed,
            "name": name,
            "success_data": succ,
            "failed_data": fail
        }, ensure_ascii=False)
        logger.info(d)
        f.write(d)


def main():
    runner()
    logger.info('start explode')
    r = redis.Redis(host='localhost', port=6379, db=0)
    with ThreadPoolExecutor(max_workers=1) as executor:
        obj_list = []
        while r.exists('url_signal_x'):
            site_data = r.rpop('url_signal_x')
            obj_list.append(executor.submit(exec, site_data))

        # 阻塞
        for task in as_completed(obj_list):
            _ = task.result()


if __name__ == '__main__':
    main()