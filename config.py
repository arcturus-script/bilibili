config = {
    "multi": [
        {
            "cookie": "xxx",
            "options": {
                "watch": True,  # 每日观看视频
                "coins": 1,  # 投币个数
                "share": True,  # 视频分享
                "comics": True,  # 漫画签到
                "lb": True,  # 直播签到
                "threshold": 100,  # 仅剩多少币时不再投币(不写默认100)
                "toCoin": False,  # 银瓜子兑换硬币
            },
            # "push": {
            #     "type": "pushplus",
            #     "key": "xxx",
            # },
        },
        {
            "cookie": "xxx",
            "options": {
                "watch": True,  # 每日观看视频
                "coins": 2,  # 投币个数
                "share": True,  # 视频分享
                "comics": True,  # 漫画签到
                "lb": True,  # 直播签到
                "toCoin": False,  # 银瓜子兑换硬币
            },
            # "push": [
            #     # 以数组的形式填写, 则会向多个服务推送消息
            #     {
            #         "type": "pushplus",
            #         "key": "xxx",
            #     },
            #     {
            #         "type": "workWechat",
            #         "key": {
            #             "agentid": 1000002,
            #             "corpSecret": "xxx",
            #             "corpid": "xxx",
            #         },
            #     },
            # ],
        },
    ],
    "push": {
        # 合并发送消息, 只合并未单独配置 push 的账号
        "type": "pushplus",
        "key": "xxx",
    },
}
