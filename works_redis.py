# coding: utf-8

import redis
from post_url_to_archive import post_url_to_archive
from check_url_backup_state import check_url_backup
import logger as log
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)
r1 = redis.Redis(host='localhost', port=6379, db=1)


def get_times():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


while True:
    data = json.loads(r.blpop("work_list")[1])
    sitemap_host = data["site_host"]
    sitemap_url = data["sitemap_url"]
    signal_all_json = {
        "sitemap_url": sitemap_url,
        "site_host": sitemap_host,
        "success_data": [],
        "failed_data": []
    }
    log.logger_info("开始处理博客：" + sitemap_host + "  " + get_times())
    data_list = data["sitemap_list"]
    for j in data_list:
        if post_url_to_archive(j):
            log.logger_info("post_url_to_archive: %s" % sitemap_url)
        if check_url_backup(j):
            signal_all_json["success_data"].append(j)
            log.logger_success("success_url_backup: %s" % sitemap_url)
        else:
            signal_all_json["failed_data"].append(j)
            log.logger_error("failed_url_backup: %s" % sitemap_url)
    log.logger_success("处理博客成功！：" + sitemap_host + "  " + get_times())
    r1.set(sitemap_host, json.dumps(signal_all_json))
