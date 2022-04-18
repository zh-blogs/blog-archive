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
from post_url_to_archive import post_url_to_archive
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


@app.get("/", summary="Home", tags=["HomePage"], include_in_schema=False)
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
    若网址已存在于提交队列中，则返回400状态码\n
    若提交队列中不存在该域名的 SiteMap 则推送该 Sitemap 至 Redis 任务队列\n
    一般2小时后即可通过 `/check` 接口查询到\n
    `:param` sitemap 网址 \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    if not isinstance(sitemap, str):
        lg.logger.error('params must be a str')
        return {'message': 'Fast API: params must be a str'}
    return post_sitemap_to_work(sitemap)


# get 检查网址归档状态
@app.get("/check", summary="检查域名归档状态", tags=["Check"])
def main(url: str = "icodeq.com"):
    """
    提交单个域名的 sitemap 返回解析后的网址列表 \n
    因为缓存原因，个别不准，推荐将失败的去请求一次 `/page_check` 接口来获取最新数据\n
    `:param` 站点域名：示例 `icodeq.com` `www.baidu.com` \n
    `:return` 解析后的网址列表
    返回数据 code 为： 404 表示该域名未在归档集合中发现
    返回数据 code 为： 201 表示该域名在归档队列中但为归档完成（或正在归档中）
    返回数据 code 为： 200 表示该域名归档成功
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
    即中转 `https://archive.org/wayback/available?url=` 的请求 \n
    `:param` 站点页面示例：https://icodeq.com/2022/bfdcaafa69d7/ \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    if not isinstance(url, str):
        lg.logger.error('params must be a str')
        return {'message': 'Fast API: params must be a str'}
    return get_page_state(url)


# get 推送单个网页进行归档
@app.get("/page_archive", summary="将单个网址进行归档", tags=["Archive"])
def main(url: str = "https://icodeq.com/2022/bfdcaafa69d7/"):
    """
    提交单个页面， 尝试将其进行归档推送，并返回查询结果\n
    但是仍然有延迟，建议不要再次出现重试按钮....\n
    `:param` 站点页面示例：https://icodeq.com/2022/bfdcaafa69d7/ \n
    `:return` 解析后的网址列表
    """
    lg.logger.info('-' * 20 + '开始记录日志' + '-' * 20)
    if not isinstance(url, str):
        lg.logger.error('params must be a str')
        return {'message': 'Fast API: params must be a str'}
    if post_url_to_archive(url):
        lg.logger_info("post_url_to_archive: %s" % url)
    data = get_page_state(url)
    return data


# 统计当前网站的状态
@app.get("/state", summary="统计当前网站的状态", tags=["State"])
def main():
    """
    统计当前网站的状态 \n
    `:return` 解析后的网址列表\n
    `all_runner_state` 表示成功提交到归档列表的域名 （下面两个的和 + 正在运行的域名）\n
    `suc_runner_state` 表示成功归档的域名\n
    `work_list` 表示在归档等待状态的域名
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
