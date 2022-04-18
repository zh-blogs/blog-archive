# coding:utf-8
import requests
import logger as log
from fake_useragent import UserAgent
import time

# mirror_base_url = os.environ['MIRROR_BASE_URL']


def check_url_backup(url):
    # return True
    # _full_url = mirror_base_url + "https://archive.org/wayback/available?url=" + url
    ua = UserAgent().chrome
    headers = {"User-Agent": ua}
    _full_url = "https://archive.org/wayback/available?url=" + url
    try:
        check_data = requests.get(_full_url, headers=headers).json()
        log.logger_info("成功检查，正在休眠 2 秒，防止频率过大")
        time.sleep(2)
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
        return True
    else:
        log.logger_error("未通过网页入库检查：" + url)
        return False
