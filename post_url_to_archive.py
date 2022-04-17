# coding:utf-8
# import os
import requests
import logger as log
from fake_useragent import UserAgent
from urllib.parse import urlparse
import time



# mirror_base_url = os.environ['MIRROR_BASE_URL']


def post_url_to_archive(url):
    ua = UserAgent().chrome
    pure_domain = urlparse(url).netloc
    headers = {"User-Agent": ua}
    _full_url = "https://web.archive.org/save/" + pure_domain
    data = {
        "url": url,
        "capture_outlinks": "on",
        "capture_all": "on",
        "capture_screenshot": "on"
    }
    log.logger_info("post_url_to_archive_ing: " + _full_url)
    try:
        r = requests.post(_full_url, data=data, headers=headers, timeout=12)
        log.logger_info("成功推送，正在休眠 2 秒，防止频率过大")
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
