# coding: utf-8
import subprocess

start_runner = "python runner.py"
start_redis = "redis/src/redis-server redis/redis.conf"
start_works = "python works_redis.py"
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from get_page_state import get_page_state
from post_sitemap_to_work import post_sitemap_to_work
import logger as lg
from sitemap_check import sitemap_check
from site_state import get_site_state
from get_runner_state import get_runner_state

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Home", tags=["HomePage"])
def main():
    return {"docs": "https://zh-blogs.icodeq.com/docs"}


@app.get("/sitemap", summary="提交单个网址的 sitemap 并获取解析后的网址列表", tags=["SiteMap"])
def main(sitemap: str = "https://icodeq.com/sitemap.xml"):
    """
    提交单个网址的 sitemap 返回解析后的网址列表 \n
    `:param` sitemap 网址 \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    if not isinstance(sitemap, str):
        lg.logger.error('params must be a str')
        return {'message': 'Fast API: params must be a str'}
    return sitemap_check(sitemap)


# post 請求來接收 sitemap
@app.post("/sitemap", summary="确认提交 SiteMap，将任务推送至 Redis", tags=["SiteMap"])
def main(sitemap: str = "https://icodeq.com/sitemap.xml"):
    """
    提交单个网址的 sitemap 返回解析后的网址列表 \n
    若前面的GET请求提交时间少于10分钟，则返回上次解析的结果 \n
    反之，则重新解析 \n
    `:param` sitemap 网址 \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    if not isinstance(sitemap, str):
        lg.logger.error('params must be a str')
        return {'message': 'Fast API: params must be a str'}
    return post_sitemap_to_work(sitemap)


# get 检查网址归档状态
@app.get("/check", summary="检查网址归档状态", tags=["Check"])
def main(url: str = "icodeq.com"):
    """
    提交单个网址的 sitemap 返回解析后的网址列表 \n
    `:param` 站点域名：示例 `icodeq.com` `www.baidu.com` \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    if not isinstance(url, str):
        lg.logger.error('params must be a str')
        return {'message': 'Fast API: params must be a str'}
    return get_site_state(url)


# get 检查网址归档状态
@app.get("/page_check", summary="检查单个子页面归档状态", tags=["Check"])
def main(url: str = "https://icodeq.com/2022/bfdcaafa69d7/"):
    """
    提交单个页面， 返回网址是否已经归档成功 \n
    `:param` 站点页面示例：https://icodeq.com/2022/bfdcaafa69d7/ \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    if not isinstance(url, str):
        lg.logger.error('params must be a str')
        return {'message': 'Fast API: params must be a str'}
    return get_page_state(url)


# 统计当前网站的状态
@app.get("/state", summary="统计当前网站的状态", tags=["State"])
def main():
    """
    统计当前网站的状态 \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    return get_runner_state()


if __name__ == "__main__":
    print("start redis")
    subprocess.Popen(start_redis, shell=True)
    subprocess.Popen(start_works, shell=True)
    subprocess.Popen(start_works, shell=True)
    subprocess.Popen(start_works, shell=True)
    subprocess.Popen(start_works, shell=True)
    subprocess.Popen(start_works, shell=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
