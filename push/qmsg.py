import requests


class qmsg:
    """
    qmsg(https://qmsg.zendee.cn/api)
    """

    def __init__(self, key) -> None:
        self.key = key
        self.url = f"https://qmsg.zendee.cn:443/send/{self.key}"

    def push_msg(self, msg) -> None:
        """
        Parameters:
            msg: 消息内容
        """
        params = {"msg": msg}
        res = requests.get(self.url, params=params).json()
        if res["code"] == 0:
            print("消息推送成功")
        else:
            print(f"推送错误, {res['info']}")
