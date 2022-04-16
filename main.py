# coding:utf-8
import time

from feed_url_to_list import feed_url_to_list
from post_url_to_archive import post_url_to_archive
from check_url_backup_state import check_url_backup
import logger as log

demo_feed = ["https://juantu.cn/feed"]


def list_to_all_links(_url_list):
    all_links = []
    for url in _url_list:
        signal_dict = feed_url_to_list(url)
        all_links.append(signal_dict)
    return all_links


if __name__ == '__main__':
    all_list = list_to_all_links(demo_feed)
    for i in all_list:
        blog_title = i["title"]
        log.logger_info("blog_title: %s" % blog_title)
        blog_url = i["link"]
        log.logger_info("blog_url: %s" % blog_url)
        for j in i["data"]:
            link_url = j["link"]
            log.logger_info("link_url: %s" % link_url)
            link_title = j["title"]
            log.logger_info("link_title: %s" % link_title)
            if post_url_to_archive(link_url):
                log.logger_info("post_url_to_archive: %s" % link_url)
            link_url = j["link"]
            log.logger_info("check_link_url: %s" % link_url)
            link_title = j["title"]
            log.logger_info("check_link_title: %s" % link_title)
            if check_url_backup(link_url):
                log.logger_success("success_url_backup: %s" % link_url)
            else:
                log.logger_error("failed_url_backup: %s" % link_url)
    print("全部执行完毕！")
