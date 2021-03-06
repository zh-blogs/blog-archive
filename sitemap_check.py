# coding:utf-8
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logger as log
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

headers = {
    "User-Agent":
    "Mozilla/5.0(compatible; zhblogBot/1.0; + https://zhblogs.ohyee.cc)"
}


def sitemap_check(sitemap_url):
    try:
        data = requests.get(sitemap_url, headers=headers)
        log.logger_info("sitemap_url:%s" % sitemap_url)
    except Exception as e:
        log.logger.error("get_url_list error: %s" % sitemap_url)
        log.logger_error(e)
        return {"status": False, "msg": "get_url_list error: %s" % sitemap_url}
    parcala = BeautifulSoup(data.content, "xml")
    loc_tags = parcala.find_all('loc')
    url_list = []
    # 解析xml文件
    for loc in loc_tags:
        url_content = loc.get_text()
        if ".xml" in url_content:
            url_list.extend(sitemap_check(url_content)["sitemap_list"])
        url_list.append(url_content)
    site_host = urlparse(sitemap_url).netloc
    data_dict = {
        "message": "SUCCESS",
        "status": True,
        "code": 200,
        "sitemap_url": sitemap_url,
        "site_host": site_host,
        "sitemap_list": url_list
    }
    r.set(site_host, json.dumps(data_dict), ex=60 * 10)
    return data_dict
