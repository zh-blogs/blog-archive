# coding:utf-8
import json

import fresh_data_from_zhblog as fd
import logger as log
from urllib.parse import urlparse
import os
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

work_news_list = []

new_data = fd.get_api_save_local()
if os.path.exists('dist/data_old.json'):
    with open('dist/data_old.json', 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    if not fd.check_data_len("dist/data_old.json", "dist/data_new.json"):
        work_news_list.append(fd.more_data_chose_new(old_data, new_data))
    work_news_list.append(fd.chose_wait_list_data(new_data))
else:
    work_news_list = new_data


# 获取 dist/detail/ 子目录下的所有文件名
def get_all_files(path):
    _site_all_urls = []
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)):
            _site_all_urls.append(file_name)
    return _site_all_urls


site_done = get_all_files('dist/detail')

log.logger_debug(site_done)

for i in site_done:
    done_i = i.replace(".json", "")
    site_done[site_done.index(i)] = done_i
    log.logger_debug(done_i)

for i in work_news_list:
    site_url = i["url"]
    link_site_url = urlparse(site_url).netloc
    log.logger_debug(f"site_url: {link_site_url}")
    if link_site_url in site_done:
        log.logger_debug("检测到已存在站点，跳过该站点")
        continue
    i = str(i)
    r.rpush("url_signal", i)
