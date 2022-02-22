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
    
3. 从头开始-函数名称随意

    > 这里选择 python3.6!!! 除非你自己会上传依赖

    [![HzKwz4.png](https://s4.ax1x.com/2022/02/22/HzKwz4.png)](https://imgtu.com/i/HzKwz4)

4. 改入口函数为 index.main

    [![HznLHP.png](https://s4.ax1x.com/2022/02/22/HznLHP.png)](https://imgtu.com/i/HznLHP)
    
5. 改超时时间(如果出现什么 timeout 什么 3 secords 就改，没有也可以不改)

    [![Hzum34.png](https://s4.ax1x.com/2022/02/22/Hzum34.png)](https://imgtu.com/i/Hzum34)

6. 顺便把推送服务的密钥也加进去

    [![HzuwDI.png](https://s4.ax1x.com/2022/02/22/HzuwDI.png)](https://imgtu.com/i/HzuwDI)

7. 改配置文件

    [![HzKxyj.png](https://s4.ax1x.com/2022/02/22/HzKxyj.png)](https://imgtu.com/i/HzKxyj)

## push

1. workWechatRobot(企业微信群机器人)
2. pushplus
3. workWechat(企业微信)
4. server

### 环境变量

[![5gTYut.png](https://z3.ax1x.com/2021/10/23/5gTYut.png)](https://imgtu.com/i/5gTYut)

环境变量 key 值与推送类型相同，对应于各个推送的密钥：

[![HzQ0bR.png](https://s4.ax1x.com/2022/02/22/HzQ0bR.png)](https://imgtu.com/i/HzQ0bR)

1. pushplus
2. server
3. workWechatRobot

企业微信有所不同，需要：

1. agentid

2. corpSecret

   [![HzQAEt.png](https://s4.ax1x.com/2022/02/22/HzQAEt.png)](https://imgtu.com/i/HzQAEt)

3. corpid

   [![HzMv4K.png](https://s4.ax1x.com/2022/02/22/HzMv4K.png)](https://imgtu.com/i/HzMv4K)

> 手动退出 bilibili 时 cookies 会失效

### 参考资料
1. [sanshuifeibing/ExampleForSCF](https://github.com/sanshuifeibing/ExampleForSCF)
2. [kamiyan233/bilibili-helper](https://github.com/kamiyan233/bilibili-helper)
