import requests as req
from re import compile
import time


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
        if watch:
            content.append(
                {
                    "txt": {
                        "content": watch["msg"],
                    }
                }
            )
        
        share = res.get("share")
        if share:
            content.append(
                {
                    "txt": {
                        "content": f"分享视频: {share}",
                    }
                }
            )

        coins = res.get("coins")
        if coins:
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
        if comics:
            if comics["status"]:
                content.extend(
                    [
                        {
                            "h5": {
                                "content": "漫画签到",
                            },
                            "txt": {
                                "content": comics['msg'],
                            },
                        },
                        {
                            "txt": {
                                "content": f"连续签到 {comics['day_count']} 天",
                            }
                        },
                    ]
                )
            else:
                content.append(
                    {
                        "h5": {
                            "content": "漫画签到",
                        },
                        "txt": {
                            "content": comics["msg"],
                        },
                    }
                )

        lb = res.get("lb")
        if lb:
            if lb["status"]:
                content.extend(
                    [
                        {
                            "h5": {
                                "content": "直播",
                            },
                            "txt": {"content": lb["raward"]},
                        },
                    ]
                )
            else:
                content.append(
                    {
                        "h5": {
                            "content": "直播",
                        },
                        "txt": {"content": lb["msg"]},
                    }
                )

        return content

    return inner


class BiliBiliAPI:
    # 获取视频信息地址
    VIDEO_INFO = "https://api.bilibili.com/x/web-interface/view"
    # 获取用户信息
    PERSONAL_INFO = "http://api.bilibili.com/x/space/myinfo"
    # 直播签到
    LIVE_BROADCAST = "https://api.live.bilibili.com/sign/doSign"
    # 漫画签到
    COMICS = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
    # 漫画签到信息
    COMICS_INFO = "https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo"
    # 获取热门推荐
    RECOMMAND = "https://api.bilibili.com/x/web-interface/popular"
    # 客户端分享视频
    VIDEO_SHARE = "https://api.bilibili.com/x/web-interface/share/add"
    # 投币
    COIN = "https://api.bilibili.com/x/web-interface/coin/add"
    # 看视频
    VIDEO_CLICK = "https://api.bilibili.com/x/click-interface/click/web/h5"
    VIDEO_HEARTBEAT = "https://api.bilibili.com/x/click-interface/web/heartbeat"


class BiliBili:
    headers = {
        "user-agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.bilibili.com/",
    }

    def __init__(self, cookie) -> None:
        self.sid = BiliBili.extract("sid", cookie)
        self.csrf = BiliBili.extract("bili_jct", cookie)
        self.uid = BiliBili.extract("DedeUserID", cookie)
        self.headers.update({"Cookie": cookie})

    @staticmethod
    def extract(key: str, cookie: str):
        """根据键从 cookie 中抽取数据

        Args:
            key: 需要抽取数据的键, 可能值 bili_jct, sid, DedeUserID
            cookie (str): BiliBili 的 cookie
        """
        regEx = compile(f"(?<={key}=).+?(?=;)|(?<={key}=).+")
        csrf = regEx.findall(cookie)
        if len(csrf) != 0:
            return csrf[0]
        else:
            return ""

    # 获取视频信息
    @staticmethod
    def get_video_info(bv):
        try:
            params = {
                "bvid": bv,
            }
            rep = req.get(
                BiliBiliAPI.VIDEO_INFO,
                params=params,
                headers=BiliBili.headers,
            ).json()

            if rep["code"] == 0:
                data = rep["data"]

                return {
                    "bvid": data["bvid"],  # 视频 BV 号
                    "aid": data["aid"],  # 视频 AV 号
                    "duration": data["duration"],
                    "cid": data["cid"],
                    "title": data["title"],  # 视频标题
                }
            else:
                print(f"获取视频信息失败, 原因: {rep['message']}")
        except Exception as ex:
            print(f"获取视频信息时出错, 原因: {ex}")

    # 获取用户信息
    def get_user_info(self):
        try:
            rep = req.get(
                BiliBiliAPI.PERSONAL_INFO,
                headers=self.headers,
            ).json()

            if rep["code"] == 0:
                data = rep["data"]

                current_exp = data["level_exp"]["current_exp"]
                next_exp = data["level_exp"]["next_exp"]

                self.name = data["name"]  # 用户名
                self.level = data["level"]  # 等级
                self.coin = data["coins"]  # 硬币数
                self.exp = f"{current_exp}/{next_exp}"  # 经验
                self.silence = data["silence"]  # 不知道是什么

            else:
                print(f"获取用户信息失败, 原因: {rep['message']}")
                self.name = "获取失败.."
                self.level = "lv0"
                self.coin = 0
                self.exp = "0/0"
                self.silence = "..."
        except Exception as ex:
            print(f"获取用户信息时出错, 原因: {ex}")
            self.name = "获取失败.."
            self.level = "lv0"
            self.coin = 0
            self.exp = "0/0"
            self.silence = "..."

    # 直播签到
    def live_broadcast_checkin(self):
        try:
            rep = req.get(
                BiliBiliAPI.LIVE_BROADCAST,
                headers=self.headers,
            ).json()

            if rep["code"] == 0:
                # 签到成功
                data = rep["data"]

                print(
                    "直播签到成功🎉🎉",
                    f"获得奖励: {data['text']}",
                    sep="\n",
                )

                return {
                    "status": True,
                    "raward": data["text"],
                    "specialText": data["specialText"],
                }
            else:
                print(f"直播签到失败, 原因: {rep['message']}")
                return {
                    "status": False,
                    "msg": rep["message"],
                }
        except Exception as ex:
            print(f"直播签到出错, 原因: {ex}")
            return {
                "status": False,
                "msg": f"直播签到出错, 原因: {ex}",
            }

    # 漫画签到
    def comics_checkin(self):
        try:
            data = {
                "platform": "android",
            }
            rep = req.post(
                BiliBiliAPI.COMICS,
                headers=self.headers,
                data=data,
            ).json()

            if rep["code"] == 0:
                print("漫画签到成功🎉🎉")

                result = self.comics_checkin_info()

                if result is not None:
                    return {
                        "status": True,
                        "msg": "签到成功",
                        "day_count": result,
                    }
                else:
                    return {
                        "status": True,
                        "msg": "签到成功",
                        "day_count": "未知...",
                    }

            elif rep["code"] == "invalid_argument":
                print("漫画签到失败, 重复签到了")
                return {
                    "status": False,
                    "msg": "签到失败, 重复签到",
                }
            else:
                return {
                    "status": False,
                    "msg": "签到失败, 未知错误",
                }
        except Exception as ex:
            print(f"漫画签到时出现错误, 原因: {ex}")
            return {
                "status": False,
                "msg": f"签到出现错误, 原因: {ex}",
            }

    def comics_checkin_info(self):
        rep = req.post(
            BiliBiliAPI.COMICS_INFO,
            headers=self.headers,
        ).json()

        if rep["code"] == 0:
            print(
                "🐼 获取漫画签到信息成功",
                f"您已经连续签到{rep['data']['day_count']}天",
                sep="\n",
            )
            return rep["data"]["day_count"]
        else:
            print(f"获取漫画签到信息失败, 原因: {rep['msg']}")

    # 获取推荐视频
    @staticmethod
    def video_suggest(ps: int = 50, pn: int = 1) -> list or None:
        """
        Args:
            ps (int): 视频个数
            pn (int): 第几页数据

        Returns:
            video_list: 一个列表, 例如
            [
                {"aid": 551162867, "title": "2022我的世界拜年纪", "bvid": xxx},
                {"aid": 508722277, "title": "B站UP主, 办了个电影节", "bvid": yyy},
                ...
            ]
        """
        params = {
            "ps": ps,
            "pn": pn,
        }
        rep = req.get(
            BiliBiliAPI.RECOMMAND,
            params=params,
        ).json()

        if rep["code"] == 0:
            video_list = []
            videos = rep["data"]["list"]

            for video in videos:
                # 将视频主要信息保存到字典里
                video_list.append(
                    {
                        "aid": video["aid"],
                        "bvid": video["bvid"],
                        "title": video["title"],
                    }
                )

            return video_list
        else:
            print(f"获取视频推荐列表失败")
            return []

    # 投币
    def give_coin(
        self,
        video_list,
        total_coin_num: int,
        per_coin_num: int = 1,
        select_like=0,
    ):
        coined_num = 0  # 已经投币数
        coin_video_list = []
        for video in video_list:
            data = {
                "aid": str(video["aid"]),
                "multiply": per_coin_num,  # 每次投币多少个, 默认 1 个
                "select_like": select_like,  # 是否同时点赞, 默认不点赞
                "cross_domain": "true",
                "csrf": self.csrf,
            }

            # 当已投币数超过想投币数时退出
            if coined_num < total_coin_num:
                rep = req.post(
                    BiliBiliAPI.COIN,
                    headers=self.headers,
                    data=data,
                ).json()

                if rep["code"] == 0:
                    # 投币成功
                    print(f"🐼 给[{video['title']}]投币成功")

                    coin_video_list.append(video["title"])

                    coined_num += 1  # 投币次数加 1
                else:
                    # 投币失败
                    print(f"给[{video['title']}]投币失败, 原因: {rep['message']}")
            else:
                print(f"投币结束, 总共投了 {coined_num} 个硬币")
                break
        return coin_video_list

    # 分享视频
    def share_video(self, video_list):
        for video in video_list:
            # 分享视频
            data = {
                "aid": video["aid"],
                "csrf": self.csrf,
            }

            rep = req.post(
                BiliBiliAPI.VIDEO_SHARE,
                data=data,
                headers=self.headers,
            ).json()

            if rep["code"] == 0:
                # 如果分享成功, 退出循环
                # 并返回分享的视频名
                print(f"分享视频[{video['title']}]成功")
                return video["title"]
            else:
                print(f"分享视频[{video['title']}]失败, 原因: {rep['message']}")

        return "无..."

    # 每日看视频
    def watch(self, bvid):
        video_info = BiliBili.get_video_info(bvid)

        # 获取视频信息成功
        if video_info:
            data = {
                "aid": video_info["aid"],
                "cid": video_info["cid"],
                "part": 1,
                "ftime": int(time.time()),
                "jsonp": "jsonp",
                "mid": self.uid,
                "csrf": self.csrf,
                "stime": int(time.time()),
            }
            rep = req.post(
                BiliBiliAPI.VIDEO_CLICK,
                data=data,
                headers=self.headers,
            ).json()

            # 进入视频页
            if rep["code"] == 0:
                data = {
                    "aid": video_info["aid"],
                    "cid": video_info["cid"],
                    "jsonp": "jsonp",
                    "mid": self.uid,
                    "csrf": self.csrf,
                    "played_time": 0,
                    "pause": False,
                    "play_type": 1,
                    "realtime": video_info["duration"],
                    "start_ts": int(time.time()),
                }
                rep = req.post(
                    BiliBiliAPI.VIDEO_HEARTBEAT,
                    data=data,
                    headers=self.headers,
                ).json()

                if rep["code"] == 0:
                    # 模拟观看视频
                    time.sleep(5)
                    data["played_time"] = video_info["duration"] - 1
                    data["play_type"] = 0
                    data["start_ts"] = int(time.time())

                    rep = req.post(
                        BiliBiliAPI.VIDEO_HEARTBEAT,
                        data=data,
                        headers=self.headers,
                    ).json()

                    if rep["code"] == 0:
                        print(f"🐼 观看视频[{video_info['title']}]成功")
                        return {
                            "status": True,
                            "msg": f"观看视频[{video_info['title']}]成功",
                        }

            print("观看视频失败")
            return {
                "status": False,
                "msg": f"观看视频[{video_info['title']}]失败",
            }

    @handler
    def start(self, options):
        self.get_user_info()  # 获取用户信息

        if options is not None:
            watch = options.get("watch")
            coins = options.get("coins")
            share = options.get("share")
            comics = options.get("comics")
            lb = options.get("lb")
            threshold = options.get("threshold", 100)

            videos = self.video_suggest()  # 获取热门视频

            if watch:  # 如果需要观看视频
                if len(videos) == 0:
                    watch_res = self.watch("BV1LS4y1C7Pa")  # 如果获取热门视频失败, 就看这个默认的视频
                else:
                    watch_res = self.watch(videos[0]["bvid"])  # 否则看第一个热门视频
            else:
                watch_res = None

            # 当用户的硬币大于阈值时才进行投币
            if coins and (self.coin - coins > threshold):
                # 获取投币成功的视频标题列表
                coin_list = self.give_coin(videos, coins)
            else:
                coin_list = None

            if share:
                # 视频分享, 如果获取热门视频失败, 则分享不了
                share_video = self.share_video(videos)
            else:
                share_video = None

            if comics:
                # 漫画签到
                comics_res = self.comics_checkin()
            else:
                comics_res = None

            if lb:
                # 直播签到
                lb_res = self.live_broadcast_checkin()
            else:
                lb_res = None

            return {
                "name": self.name,
                "level": self.level,
                "coin": self.coin,
                "exp": self.exp,
                "coins": coin_list,
                "share": share_video,
                "comics": comics_res,
                "lb": lb_res,
                "watch": watch_res,
            }
        else:
            return {
                "name": self.name,
                "level": self.level,
                "coin": self.coin,
                "exp": self.exp,
            }
