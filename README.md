- demo地址：https://zh-blogs.icodeq.com
- 文档地址：https://zh-blogs.icodeq.com/docs

### 接口文档

#### SiteMap: 提交单个网址的 sitemap 并获取解析后的网址列表

`GET /sitemap`

- 提交单个网址的 sitemap 返回解析后的网址列表

`:param` sitemap 网址

`:return` 解析后的网址列表

##### 请求参数

| 参数名  | 位置  | 类型   | 必填 | 说明 |
| :------ | :---- | :----- | :--: | :--- |
| sitemap | query | string |  否  |      |

#### SiteMap: 确认提交 SiteMap，将任务推送至 Redis

`POST /sitemap`

- 提交单个网址的 sitemap 返回解析后的网址列表

- 若前面的GET请求提交时间少于10分钟，则返回上次解析的结果

- 反之，则重新解析

- 若网址已存在于提交队列中，则返回400状态码

- 若提交队列中不存在该域名的 SiteMap 则推送该 Sitemap 至 Redis 任务队列

- 一般2小时后即可通过 `/check` 接口查询到

`:param` sitemap 网址

`:return` 解析后的网址列表

##### 请求参数

| 参数名  | 位置  | 类型   | 必填 | 说明 |
| :------ | :---- | :----- | :--: | :--- |
| sitemap | query | string |  否  |      |

#### Check: 检查域名归档状态

`GET /check`

- 提交单个域名的 sitemap 返回解析后的网址列表

- 因为缓存原因，个别不准，推荐将失败的去请求一次 `/page_check` 接口来获取最新数据

`:param` 站点域名：示例 `icodeq.com` `www.baidu.com

`:return` 解析后的网址列表

- 返回数据 code 为： 404 表示该域名未在归档集合中发现

- 返回数据 code 为： 201 表示该域名在归档队列中但为归档完成（或正在归档中）

- 返回数据 code 为： 200 表示该域名归档成功

##### 请求参数

| 参数名 | 位置  | 类型   | 必填 | 说明 |
| :----- | :---- | :----- | :--: | :--- |
| url    | query | string |  否  |      |

#### Check: 检查单个子页面归档状态

`GET/page_check`

- 提交单个页面， 返回网址是否已经归档成功

- 即中转 `https://archive.org/wayback/available?url=` 的请求

`:param` 站点页面示例：https://icodeq.com/2022/bfdcaafa69d7/

`:return` 解析后的网址列表

##### 请求参数

| 参数名 | 位置  | 类型   | 必填 | 说明 |
| :----- | :---- | :----- | :--: | :--- |
| url    | query | string |  否  |      |

#### Archive: 将单个网址进行归档

`GET /page_archive`

- 提交单个页面， 尝试将其进行归档推送，并返回查询结果

- 但是仍然有延迟，建议不要再次出现重试按钮....

`:param` 站点页面示例：https://icodeq.com/2022/bfdcaafa69d7/

`:return` 解析后的网址列表

##### 请求参数

| 参数名 | 位置  | 类型   | 必填 | 说明 |
| :----- | :---- | :----- | :--: | :--- |
| url    | query | string |  否  |      |

#### State: 统计当前网站的状态

`GET /state`

- 统计当前网站的状态

`:return` 解析后的网址列表

- `all_runner_state` 表示成功提交到归档列表的域名 （下面两个的和 + 正在运行的域名）

`- suc_runner_state` 表示成功归档的域名

- `work_list` 表示在归档等待状态的域名