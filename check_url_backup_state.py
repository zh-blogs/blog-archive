# coding:utf-8
import os
import requests
import logger as log
import time

# mirror_base_url = os.environ['MIRROR_BASE_URL']


def check_url_backup(url):
    # _full_url = mirror_base_url + "https://archive.org/wayback/available?url=" + url
    _full_url = "https://archive.org/wayback/available?url=" + url
    try:
        check_data = requests.get(_full_url).json()
        time.sleep(1)
    except Exception as e:
        log.logger_error("check_url_success error: %s" % url)
        log.logger_error(e)
        return None
    try:
        result = check_data["archived_snapshots"]["closest"]["available"]
        url = check_data["archived_snapshots"]["closest"]["url"]
    except Exception as e:
        log.logger_error("check_url_success error: %s" % url)
        log.logger_error(e)
        result = False
    if result:
        log.logger_info("已查询到网页成功入库！：" + url)
        return True, url
    else:
        log.logger_error("未通过网页入库检查：" + url)
        return False, url
