<div align="center">
<h1>BiliBili签到-腾讯云函数</h1>
</div>
### 实现功能

- [x] 获取用户信息
- [x] 直播签到
- [x] 漫画签到
- [x] 投币
- [x] 分享视频
- [x] 每日看视频
- [x] 多账户支持

### 参数

> 需要将参数填写至环境变量处

[![5gTYut.png](https://z3.ax1x.com/2021/10/23/5gTYut.png)](https://imgtu.com/i/5gTYut)

[![5gTMND.png](https://z3.ax1x.com/2021/10/23/5gTMND.png)](https://imgtu.com/i/5gTMND)

|         key         | 类型 |        value        |                            描述                             |
| :-----------------: | :--: | :-----------------: | :---------------------------------------------------------: |
|       Cookies       | 必填 |          -          |                     多账户使用 `,` 分割                     |
|      push_type      | 选填 |       0 1 2 3       |                    推送类型，默认不推送                     |
|         bid         | 选填 | 默认 `BV1if4y1g7Qp` |          每日观看视频的 BV 号<br />不填不进行观看           |
|     want_watch      | 选填 |       0 或 1        |                      是否进行每日观看                       |
|    want_coin_num    | 选填 |   推荐不多于 5 个   | 每天投多少个硬币<br />因为只有前5个有经验<br />投币视频随机 |
|   want_share_num    | 选填 |       0 或 1        |                      是否进行视频分享                       |
| want_comics_checkin | 选填 |       0 或 1        |                      是否进行漫画签到                       |
|   want_lb_checkin   | 选填 |       0 或 1        |                      是否进行直播签到                       |

> 手动退出 bilibili 时 cookies 会失效
>
> 每个 cookies 需要在末尾加一个 `;` 因为需要用正则表达式获取 uid、sid、csrf，但是 cookies 里这些排序是乱的，有时候放到末尾没有 `;` 这样就不匹配正则表达式，存在找不到 csrf 的问题，导致 csrf 校验问题...
>
> 如果您有更好的正则表达式欢迎 pr 给我

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

### 参考资料
1. [sanshuifeibing/ExampleForSCF](https://github.com/sanshuifeibing/ExampleForSCF)
2. [kamiyan233/bilibili-helper](https://github.com/kamiyan233/bilibili-helper)
