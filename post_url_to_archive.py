# coding:utf-8
import os
import time

import requests
import logger as log

mirror_base_url = os.environ['MIRROR_BASE_URL']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39"
}


def post_url_to_archive(url):
    _full_url = "https://web.archive.org/save/" + url
    data = {
        "url": url,
        "capture_outlinks": "on",
        "capture_all": "on",
        "capture_screenshot": "on"
    }
    log.logger_info("post_url_to_archive_ing: " + _full_url)
    try:
        r = requests.post(_full_url, data=data, headers=headers)
        time.sleep(1)
    except Exception as e:
        log.logger_error("post_url_to_archive error: %s" % url)
        log.logger_error(e)
        return None
    if r.status_code == 200:
        log.logger_info("网页推送成功：" + url)
        return True, url
    else:
        print(r.text)
        log.logger_error("网页归档失败，请检查: " + url)
        return False, url
