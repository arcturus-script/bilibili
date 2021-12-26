<div align="center">
<h1>BiliBili签到-腾讯云函数</h1>

[![GitHub issues](https://img.shields.io/github/issues/ICE99125/BiliBili_Checkin?color=red&style=for-the-badge)](https://github.com/ICE99125/BiliBili_Checkin/issues)  [![GitHub forks](https://img.shields.io/github/forks/ICE99125/BiliBili_Checkin?style=for-the-badge)](https://github.com/ICE99125/BiliBili_Checkin/network)  [![GitHub stars](https://img.shields.io/github/stars/ICE99125/BiliBili_Checkin?style=for-the-badge)](https://github.com/ICE99125/BiliBili_Checkin/stargazers)  [![Python](https://img.shields.io/badge/python-3.6%2B-orange?style=for-the-badge)](https://www.python.org/)
</div>


### 实现功能

- [x] 获取用户信息
- [x] 直播签到
- [x] 漫画签到
- [x] 投币
- [x] 分享视频
- [x] 每日看视频
- [x] 多账户支持

### 步骤

1. 点击进入[腾讯云控制台](https://console.cloud.tencent.com/scf/list?rid=1&ns=default)
2. 点击新建

    [![5gOxG8.png](https://z3.ax1x.com/2021/10/23/5gOxG8.png)](https://imgtu.com/i/5gOxG8)
3. 自定义创建-函数名称随意-改执行方法为 `index-main`

    [![5gOvPf.png](https://z3.ax1x.com/2021/10/23/5gOvPf.png)](https://imgtu.com/i/5gOvPf)

4. 在线编辑或者本地上传zip包都可以(上传zip包注意不要直接上传github上下载的，因为解压后代码不在一级目录下)

    [![I3xpgP.png](https://z3.ax1x.com/2021/11/08/I3xpgP.png)](https://imgtu.com/i/I3xpgP)

### 参数

> 需要将参数填写至环境变量处

[![5gTYut.png](https://z3.ax1x.com/2021/10/23/5gTYut.png)](https://imgtu.com/i/5gTYut)

[![5gTMND.png](https://z3.ax1x.com/2021/10/23/5gTMND.png)](https://imgtu.com/i/5gTMND)

|         key         | 类型 |        value        |                            描述                             |
| :-----------------: | :--: | :-----------------: | :---------------------------------------------------------: |
|       Cookies       | 必填 |          -          |                     多账户使用 `,` 分割                     |
|      push_type      | 选填 |       0 1 2 3       |                    推送类型，默认不推送                     |
|         bid         | 选填 | 默认 `BV1if4y1g7Qp` |                    每日观看视频的 BV 号                     |
|     want_watch      | 选填 |       0 或 1        |                      是否进行每日观看                       |
|    want_coin_num    | 选填 |   推荐不多于 5 个   | 每天投多少个硬币<br />因为只有前5个有经验<br />投币视频随机 |
|   want_share_num    | 选填 |       0 或 1        |                      是否进行视频分享                       |
| want_comics_checkin | 选填 |       0 或 1        |                      是否进行漫画签到                       |
|   want_lb_checkin   | 选填 |       0 或 1        |                      是否进行直播签到                       |
|         key         | 选填 |          -          |                   pushplus、server酱的key                   |

> 手动退出 bilibili 时 cookies 会失效

> 确保 cookies 中不含有 ',' 如果含有，务必将第 20 行代码  Cookies = os.getenv('Cookies').split(',') 里的分割符改成特殊的，否则会报错

#### 企业微信推送必填

|     key      |   description   |
| :----------: | :-------------: |
|   AgentId    |     应用 ID     |
|    Secret    |    应用密钥     |
|    Touser    | 不填默认 `@all` |
| EnterpriseID |     企业 ID     |

#### push_type

| key  | description |
| :--: | :---------: |
|  0   | 不使用推送  |
|  1   |  企业微信   |
|  2   |  server 酱  |
|  3   |  pushplus   |

> 使用 server 酱或 pushplus 需要在环境变量上加上 key

> server 酱排版目前有点问题 🙃 建议用 pushplus 吧

### 参考资料
1. [sanshuifeibing/ExampleForSCF](https://github.com/sanshuifeibing/ExampleForSCF)
2. [kamiyan233/bilibili-helper](https://github.com/kamiyan233/bilibili-helper)
