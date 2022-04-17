# coding: utf-8

import redis
from post_url_to_archive import post_url_to_archive
from feed_url_to_list import feed_url_to_list
from check_url_backup_state import check_url_backup
from urllib.parse import urlparse
import logger as log
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)


def get_times():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def write_wait_list(url):
    r.rpush("wait_list", url)
    # if not os.path.exists('dist/wait_list.json'):
    #     with open('dist/wait_list.json', 'w', encoding='utf-8') as _f:
    #         data = json.dumps([url])
    #         _f.write(data)
    # else:
    #     with open('dist/wait_list.json', 'r', encoding='utf-8') as _f:
    #         data = json.load(_f)
    #     data.append(url)
    #     with open('dist/wait_list.json', 'w', encoding='utf-8') as _f:
    #         data = json.dumps(data)
    #         _f.write(data)


while True:
    i = r.blpop("url_signal")[1].decode('utf-8')
    i = eval(i)
    log.logger_info("开始处理博客：" + i['name'])
    link_url = i["url"]
    feed_url = i["feed"]
    link_site_url = urlparse(link_url).netloc
    log.logger_info("link_url: %s" % link_url)
    link_title = i["name"]
    idx = i["idx"]
    log.logger_info("link_title: %s" % link_title)
    signal_all_json = {"link": link_url, "name": link_title, "update_time": get_times(), "idx": idx,
                       "feed_url": feed_url, "success_data": [], "failed_data": []}
    feed_url = i["feed"]
    if feed_url == "":
        write_wait_list(link_url)
        log.logger_info("feed_url为空，添加到待处理列表")
        continue
    sig_data = feed_url_to_list(feed_url)
    try:
        sig_data["data"]
    except TypeError:
        log.logger_info("feed_url无法获取，添加到待处理列表")
        write_wait_list(link_url)
        continue
    for j in sig_data["data"]:
        link_url = j["link"]
        link_title = j["title"]
        if post_url_to_archive(link_url):
            log.logger_info("post_url_to_archive: %s" % link_url)
        log.logger_info("check_link_url: %s" % link_url)
        log.logger_info("check_link_title: %s" % link_title)
        if check_url_backup(link_url):
            signal_all_json["success_data"].append(link_url)
            log.logger_success("success_url_backup: %s" % link_url)
        else:
            signal_all_json["failed_data"].append(link_url)
            log.logger_error("failed_url_backup: %s" % link_url)
    with open("dist/detail/{}.json".format(link_site_url), 'w', encoding='utf-8') as f:
        f.write(json.dumps(signal_all_json, ensure_ascii=False))

