# coding:utf-8

import xml.etree.ElementTree as ET
import requests
import logger as log


def feed_url_to_list(signal_feed_url):
    try:
        r = requests.get(signal_feed_url)
    except Exception as e:
        log.logger.error("get_url_list error: %s" % signal_feed_url)
        log.logger_error(e)
        return None
    try:
        root = ET.fromstring(r.content)
    except Exception as e:
        log.logger.error("xml_decode error: %s" % signal_feed_url)
        log.logger_error(e)
        return None
    try:
        signal_dict = {
                "title": root.findall("./channel/title")[0].text,
                "link": root.findall("./channel/link")[0].text,
                "data": []
                       }
    except:
        log.logger.error("xml_decode error: %s" % signal_feed_url)
        return None
    log.logger_info("正在获取链接列表：" + signal_dict["title"])
    for item in root.findall('channel/item'):
        work_data = {
                "title": item.findall("./title")[0].text,
                "link": item.findall("./link")[0].text
                }
        signal_dict["data"].append(work_data)
        log.logger_info("成功添加网页：" + work_data["link"])
    return signal_dict
