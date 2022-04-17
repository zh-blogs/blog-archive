# coding:utf-8
# 查看已存在博客的列表
# 筛选需要新发布的文章
import json
import os
from feed_url_to_list import feed_url_to_list
from post_url_to_archive import post_url_to_archive
from check_url_backup_state import check_url_backup
import logger as log


# 获取 dist/detail/ 子目录下的所有文件名
def get_all_files(path):
    _site_all_urls = []
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)):
            _site_all_urls.append(file_name)
    return _site_all_urls


def new_page_url(site_url):
    # 读取 dist/detail/site_url.json 文件
    with open(os.path.join('dist', 'detail', site_url + '.json'), 'r', encoding='utf-8') as f:
        content = json.load(f)
    xml_url = content['feed_url']
    xml_history = content['success_data']
    work_url = []
    # 获取 xml_url 对应的 xml 文件内容
    xml_content = feed_url_to_list(xml_url)
    xml_data = xml_content['data']
    for i in xml_data:
        if i['link'] not in xml_history:
            work_data = {"title": i['title'], "link": i['link']}
            work_url.append(work_data)
    return work_url


def update_works(_site_all_urls):
    for i in _site_all_urls:
        work_list = new_page_url(i)
        success_data = []
        for link_url in work_list:
            title = link_url['title']
            link = link_url['link']
            log.logger_info("link_url: %s" % link)
            if post_url_to_archive(link):
                log.logger_info("post_url_to_archive: %s" % link)
            log.logger_info("check_link_url: %s" % link)
            if check_url_backup(link):
                log.logger_success("success_url_backup: %s" % link)
                success_data.append({'title': title, 'link': link})
            else:
                log.logger_error("failed_url_backup: %s" % link)
        with open(os.path.join('dist', 'detail', i + '.json'), 'r', encoding='utf-8') as f:
            content = json.load(f)
        content['success_data'].append(success_data)
        with open(os.path.join('dist', 'detail', i + '.json'), 'w', encoding='utf-8') as f:
            data = json.dumps(content)
            f.write(data)
            log.logger_info("update_works: %s" % i)


if __name__ == '__main__':
    all_sites_list = get_all_files('dist/detail')
    site_all_urls = new_page_url(all_sites_list)
    update_works(site_all_urls)
