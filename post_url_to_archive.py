# coding:utf-8
import os
import requests
import logger as log

mirror_base_url = os.environ['MIRROR_BASE_URL']


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
        r = requests.post(_full_url, data=data)
    except Exception as e:
        log.logger_error("post_url_to_archive error: %s" % url)
        log.logger_error(e)
        return None
    if r.status_code == 200:
        log.logger_info("已查询到网页成功入库！：" + url)
        return True, url
    else:
        print(r.text)
        log.logger_error("未通过网页入库检查：" + url)
        return False, url
