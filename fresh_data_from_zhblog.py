# coding:utf-8
import json
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


def chose_wait_list_data(new_data_list):
    if os.path.exists(f'dist/wait_list.json'):
        log.logger_info("wait_list.json文件存在，开始分析是否存在 feed 数据")
        with open(f'dist/wait_list.json', 'r', encoding="utf-8") as f:
            wait_list = f.read()
    else:
        wait_list = []
    work_list = []
    for i in new_data_list:
        sig_url = i['url']
        if sig_url in wait_list:
            log.logger_info(f"{i['url']} 检测到存在 wait_list.json")
            if i['feed'] != "":
                log.logger_info(f"{i['url']} 检测到更新了 feed 数据")
                work_list.append(i)
                # FEED 提取出来之后，删除 wait_list.json 中的数据
                with open(f'dist/wait_list.json', 'r', encoding="utf-8") as f:
                    wait_list = json.load(f)
                for j in wait_list:
                    if j['url'] == sig_url:
                        wait_list.remove(i)
                with open(f'dist/wait_list.json', 'r', encoding="utf-8") as f:
                    data = json.dumps(data)
                    f.write(data)
            else:
                log.logger_info(f"{i['url']} 检测到没有更新 feed 数据")
        else:
            log.logger_info(f"{i['url']} 检测到不存在 wait_list.json")
    return work_list
