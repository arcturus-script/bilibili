import requests as req
from re import compile
from tools import failed, handler, info, success
from datetime import datetime
import time

# 获取视频信息地址
VIDEO_INFO = "https://api.bilibili.com/x/web-interface/view"

# 获取用户信息
PERSONAL_INFO = "https://api.bilibili.com/x/space/myinfo"

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

# 兑换硬币
TO_COIN = "https://api.live.bilibili.com/xlive/revenue/v1/wallet/silver2coin"

# 获取当日投币情况
COIN_LOG = " https://api.bilibili.com/x/member/web/coin/log"


class BiliBili:
    headers = {
        "user-agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.bilibili.com/",
    }

    def __init__(self, **config) -> None:
        self.cookie = config.get("cookie")
        self.options = config.get("options", {})

        self.sid = BiliBili.extract("sid", self.cookie)
        self.csrf = BiliBili.extract("bili_jct", self.cookie)
        self.uid = BiliBili.extract("DedeUserID", self.cookie)
        self.headers.update({"Cookie": self.cookie})

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
            rep = req.get(
                VIDEO_INFO,
                params={"bvid": bv},
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
                failed(f"获取视频信息失败, 原因: {rep['message']}")
        except Exception as ex:
            failed(f"获取视频信息时出错, 原因: {ex}")

    # 获取用户信息
    def get_user_info(self):
        try:
            rep = req.get(PERSONAL_INFO, headers=self.headers).json()

            if rep["code"] == 0:
                data = rep["data"]

                current_exp = data["level_exp"]["current_exp"]
                next_exp = data["level_exp"]["next_exp"]

                self.name = data["name"]  # 用户名
                self.level = data["level"]  # 等级
                self.coin = data["coins"]  # 硬币数
                self.exp = f"{current_exp}/{next_exp}"  # 经验
                self.silence = data["silence"]  # 不知道是什么
                
                success(f"获取用户信息成功, 用户: {self.name}")
            else:
                raise Exception(rep["message"])
        except Exception as ex:
            failed(f"获取用户信息时出错, 原因: {ex}")

            self.name = "Unkown"
            self.level = "lv0"
            self.coin = 0
            self.exp = "0/0"
            self.silence = "Unkown"

    # 直播签到
    def live_broadcast_checkin(self):
        if not self.options.get("lb", False):
            return

        try:
            rep = req.get(LIVE_BROADCAST, headers=self.headers).json()

            if rep["code"] == 0:
                # 签到成功
                data = rep["data"]

                success(f"直播签到: 奖励 {data['text']}")

                return {
                    "raward": data["text"],
                    "specialText": data["specialText"],
                }
            else:
                raise Exception(rep["message"])

        except Exception as ex:
            failed(f"直播签到失败, {ex}")

    # 漫画签到
    def comics_checkin(self):
        if not self.options.get("comics", False):
            return

        try:
            rep = req.post(
                COMICS,
                headers=self.headers,
                data={
                    "platform": "android",
                },
            ).json()

            if rep["code"] == 0:
                success("漫画签到完成")

                result = self.comics_checkin_info()

                if result is not None:
                    return result
                else:
                    return "unkown"
            else:
                raise Exception(rep.get("msg", "Unknown error"))
        except Exception as ex:
            failed(f"漫画签到失败, {ex}")

    def comics_checkin_info(self):
        rep = req.post(COMICS_INFO, headers=self.headers).json()

        if rep["code"] == 0:
            success(f"获取漫画签到信息成功, 您已经连续签到 {rep['data']['day_count']} 天")

            return rep["data"]["day_count"]
        else:
            failed(f"获取漫画签到信息失败, 原因: {rep['msg']}")

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

        rep = req.get(RECOMMAND, params={"ps": ps, "pn": pn}).json()

        if rep["code"] == 0:
            res = []

            videos = rep["data"]["list"]

            for video in videos:
                # 将视频主要信息保存到字典里
                res.append(
                    {
                        "aid": video["aid"],
                        "bvid": video["bvid"],
                        "title": video["title"],
                    }
                )

            return res
        else:
            failed(f"获取视频推荐列表失败")

            return [{"bvid": "BV1LS4y1C7Pa"}]

    # 投币
    def give_coin(self, videos, per_coin_num=1, select_like=0):
        coined = self.getCoinLog()  # 已经投币数

        max_coin = self.options.get("coins", 0)

        if max_coin == 0:
            return

        surplus = max_coin - coined
        surplus = 0 if surplus < 0 else surplus

        info(f"还需投币 {surplus} 个")
        
        coin_videos = []

        for video in videos:
            # 当已投币数超过想投币数时退出
            if coined < max_coin:
                data = {
                    "aid": str(video["aid"]),
                    "multiply": per_coin_num,  # 每次投币多少个, 默认 1 个
                    "select_like": select_like,  # 是否同时点赞, 默认不点赞
                    "cross_domain": "true",
                    "csrf": self.csrf,
                }

                rep = req.post(COIN, headers=self.headers, data=data).json()

                if rep["code"] == 0:
                    # 投币成功
                    success(f"给[{video['title']}]投币成功")

                    coin_videos.append(video["title"])

                    coined += 1  # 投币次数加 1
                else:
                    # 投币失败
                    failed(f"给[{video['title']}]投币失败, 原因: {rep['message']}")
            else:
                success(f"投币完成, 今日共投了 {coined} 个硬币")

                break

        return coin_videos

    # 分享视频
    def share_video(self, videos):
        if not self.options.get("share", False):
            return

        for video in videos:
            # 分享视频
            data = {
                "aid": video["aid"],
                "csrf": self.csrf,
            }

            rep = req.post(VIDEO_SHARE, data=data, headers=self.headers).json()

            if rep["code"] == 0:
                # 如果分享成功, 退出循环, 并返回分享的视频名
                success(f"分享视频完成, [{video['title']}]")

                return video["title"]
            else:
                failed(f"分享视频[{video['title']}]失败, {rep['message']}")

    # 每日看视频
    def watch(self, bvid):
        if not self.options.get("watch", False):
            return

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

            rep = req.post(VIDEO_CLICK, data=data, headers=self.headers).json()

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

                rep = req.post(VIDEO_HEARTBEAT, data=data, headers=self.headers).json()

                if rep["code"] == 0:
                    # 模拟观看视频
                    time.sleep(5)

                    data["played_time"] = video_info["duration"] - 1
                    data["play_type"] = 0
                    data["start_ts"] = int(time.time())

                    rep = req.post(
                        VIDEO_HEARTBEAT,
                        data=data,
                        headers=self.headers,
                    ).json()

                    if rep["code"] == 0:
                        success(f"观看视频完成, [{video_info['title']}]")

                        return f"观看视频[{video_info['title']}]成功"

            failed(f"观看视频失败, [{video_info['title']}]")

    # 银瓜子兑换银币
    def toCoin(self):
        if not self.options.get("toCoin", False):
            return

        resp = req.post(
            TO_COIN,
            headers=self.headers,
            data={
                "csrf_token": self.csrf,
                "csrf": self.csrf,
            },
        ).json()

        return resp.get("message", "兑换失败")

    def getCoinLog(self):
        resp = req.get(
            COIN_LOG,
            headers=self.headers,
            params={
                "csrf": self.csrf,
                "jsonp": "jsonp",
            },
        ).json()

        res = 0

        if resp.get("code") == 0:
            coin_log = resp.get("data").get("list")

            today = datetime.today().date()
            for i in coin_log:
                t = datetime.strptime(i["time"], "%Y-%m-%d %H:%M:%S")

                if t.date() == today:
                    if i["delta"] < 0:
                        res += -i["delta"]
            
            success(f"获取硬币投递情况成功, 当前已投币 {res} 个")
        else:
            failed("获取投币情况失败")

        return res

    @handler
    def start(self):
        self.get_user_info()  # 获取用户信息

        videos = self.video_suggest()  # 获取热门视频

        return {
            "name": self.name,
            "level": self.level,
            "coin": self.coin,
            "exp": self.exp,
            "coins": self.give_coin(videos),  # 投币
            "share": self.share_video(videos),  # 视频分享
            "comics": self.comics_checkin(),  # 漫画签到
            "lb": self.live_broadcast_checkin(),  # 直播签到
            "watch": self.watch(videos[0]["bvid"]),  # 观看视频
            "toCoin": self.toCoin(),  # 银瓜子兑换硬币,
        }
