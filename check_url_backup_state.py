# coding:utf-8
import os
import requests
import logger as log

# mirror_base_url = os.environ['MIRROR_BASE_URL']


def check_url_backup(url):
    # _full_url = mirror_base_url + "https://archive.org/wayback/available?url=" + url
    _full_url = "https://archive.org/wayback/available?url=" + url
    try:
        check_data = requests.get(_full_url).json()
    except Exception as e:
        log.logger.error("check_url_success error: %s" % url)
        log.logger_error(e)
        return None
    if check_data["archived_snapshots"]["closest"]["available"]:
        log.logger_info("网页已归档：" + url)
        return {url: True}
    else:
        log.logger_error("网页归档失败？请检查：" + url)
        return {url: False}
