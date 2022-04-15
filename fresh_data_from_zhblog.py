# coding:utf-8

import requests
import logger as log
import os

api_address = os.environ['SITE_API_URL']


def get_api_save_local():
    # 将api返回的json数据保存在本地
    log.logger_info("开始获取api数据")
    r = requests.get(api_address)
    with open(f'dist/data_new.json', 'w', encoding="utf-8") as f:
        f.write(r.text)
    log.logger_success(f"from api_address get data success")
    return r.text


def check_data_len(old_data, new_data):
    # 检查两个json数据的长度是否相同
    log.logger_info("开始检查两个json数据的长度是否相同")
    if len(old_data) == len(new_data):
        log.logger_info("两个json数据的长度相同")
        return True
    else:
        log.logger_info("两个json数据的长度不相同")
        return False


def more_data_chose_new(old_data, new_data):
    # 如果两个json数据的长度不相同，则选择新的数据
    log.logger_info("开始选择新的数据")
    chose_data = new_data[len(old_data):]
    return chose_data


