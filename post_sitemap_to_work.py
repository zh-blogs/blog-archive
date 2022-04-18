# coding:utf-8
import json

import redis
from sitemap_check import sitemap_check
import logger as log
from urllib.parse import urlparse

r = redis.Redis(host='localhost', port=6379, db=0)


def post_sitemap_to_work(sitemap_url):
    site_host = urlparse(sitemap_url).netloc
    sitemap_list = r.get(site_host)
    if sitemap_list:
        work_data = json.loads(sitemap_list)
    else:
        work_data = sitemap_check(sitemap_url)
    if not r.sismember('work_set', site_host):
        log.logger_success("{} is not in work_set".format(site_host))
        r.lpush('work_list', json.dumps(work_data))
        r.sadd('work_set', site_host)
        return {
            "status": True,
            "msg": "get_url_list success: %s" % sitemap_url,
            "code": 200,
            "data": work_data
        }
    else:
        log.logger_warning("{} is in work_set".format(site_host))
        return {
            "status": False,
            "message": "This URL is already in the queue! %s" % sitemap_url,
            "code": 400,
            "data": work_data}

