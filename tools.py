def handler(fn):
    def inner(*args, **kwargs):
        res = fn(*args, **kwargs)

        content = [
            {
                "h4": {
                    "content": res["name"],
                },
            },
            {
                "txt": {
                    "content": f"等级: {res['level']}",
                },
            },
            {
                "txt": {
                    "content": f"硬币: {res['coin']}",
                },
            },
            {
                "txt": {
                    "content": f"经验: {res['exp']}",
                },
            },
        ]

        watch = res.get("watch")

        if watch is not None:
            content.append(
                {
                    "txt": {
                        "content": watch,
                    }
                }
            )

        share = res.get("share")

        if share is not None:
            content.append(
                {
                    "txt": {
                        "content": f"分享视频: {share}",
                    }
                }
            )

        coins = res.get("coins")

        if coins is not None:
            content.append(
                {
                    "h5": {
                        "content": "投币",
                    },
                    "orderedList": {
                        "content": coins,
                    },
                }
            )

        comics = res.get("comics")

        if comics is not None:
            content.extend(
                [
                    {
                        "h5": {
                            "content": "漫画签到",
                        },
                        "txt": {
                            "content": f"连续签到 {comics} 天",
                        },
                    },
                ]
            )

        lb = res.get("lb")

        if lb is not None:
            content.extend(
                [
                    {
                        "h5": {
                            "content": "直播",
                        },
                        "txt": {
                            "content": lb["raward"],
                        },
                    },
                ]
            )

        toCoin = res.get("toCoin")

        if toCoin is not None:
            content.append(
                {
                    "h5": {
                        "content": "银瓜子兑换硬币",
                    },
                    "txt": {
                        "content": toCoin,
                    },
                }
            )

        return content

    return inner


def failed(*args, **kwargs):
    print("[\033[31mfailed\033[0m]  ", end="")
    print(*args, **kwargs)


def success(*args, **kwargs):
    print("[\033[32msuccess\033[0m] ", end="")
    print(*args, **kwargs)


def info(*args, **kwargs):
    print("[\033[34minfo\033[0m]    ", end="")
    print(*args, **kwargs)