<div align="center">
<h1>BiliBili签到-腾讯云函数</h1>
</div>

### 实现功能
1. 获取用户信息
2. 直播签到
3. 漫画签到
4. 投币
5. 分享视频
6. 每日看视频
7. 多账户支持

### 参数

|         键          | 类型/值  |                             描述                             |
| :-----------------: | :------: | :----------------------------------------------------------: |
|       Cookies       |   必填   |                     多账户使用 `,` 分割                      |
|        csrf         |   必填   |                      从 cookies 里面找                       |
|         uid         |   必填   |                      从 cookies 里面找                       |
|         sid         |   必填   |                      从 cookies 里面找                       |
|      push_type      |   选填   |                 推送类型,不填写默认为不推送                  |
|         bid         |   选填   |           每日观看视频的 BV 号<br />不填不进行观看           |
|     want_watch      | 选填/0,1 | 是否进行每日观看<br />多账号使用 `,` 分割<br />没有 bid 这一项无效 |
|    want_coin_num    | 选填/0~5 | 每天投多少个硬币<br />多账号使用 `,` 分割<br /><span style="color:red">投币视频随机</span> |
|   want_share_num    | 选填/0,1 |          是否进行视频分享<br />多账号使用 `,` 分割           |
| want_comics_checkin | 选填/0,1 |          是否进行漫画签到<br />多账号使用 `,` 分割           |
|   want_lb_checkin   | 选填/0,1 |          是否进行直播签到<br />多账号使用 `,` 分割           |

#### 企业微信推送必填

|   AgentId    |     应用 ID     |
| :----------: | :-------------: |
|    Secret    |    应用密钥     |
|    Touser    | 不填默认 `@all` |
| EnterpriseID |     企业 ID     |

#### push_type

|  0   | 不使用推送 |
| :--: | :--------: |
|  1   |  企业微信  |
|  2   | server 酱  |
|  3   |  pushplus  |

### 参考资料
1. [sanshuifeibing/ExampleForSCF](https://github.com/sanshuifeibing/ExampleForSCF)
2. [kamiyan233/bilibili-helper](https://github.com/kamiyan233/bilibili-helper)