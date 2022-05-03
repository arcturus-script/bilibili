config = {
    "multi": [
        {
            "cookie": "账号1",
            "options": {
                "watch": True,  # 每日观看视频
                "coins": 2,  # 投币个数
                "share": True,  # 视频分享
                "comics": True,  # 漫画签到
                "lb": True,  # 直播签到
                "threshold": 100 # 仅剩多少币时不再投币(不写默认100)
            },
            "push": "pushplus", # together 为 True 时失效, 不写不推送
        },
        # {
        #     "cookie": "账号2",
        #     "options": {
        #         "watch": True,
        #         "coins": 5,
        #         "share": True,
        #         "comics": True,
        #         "lb": True,
        #     },
        #     "push": "pushplus",
        # },
    ],
    "together": True, # 是否合并发送结果, 不写或 True 时合并发送
    "push": "pushplus", # 推送类型, together 为 True 或者不写时必须有, 否则不推送
}
