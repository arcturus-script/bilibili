import requests as re


class server:
    """
    server 酱(https://sct.ftqq.com/)
    """

    push_url = "https://sctapi.ftqq.com/"

    def __init__(self, key) -> None:
        self.key = key
        self.url = f"{server.push_url}{self.key}.send"

    def push_msg(self, title: str, **kwargs) -> None:
        """
        Parameters:
            title: 消息标题
            channel: 消息通道
            desp: 消息内容
        """
        params = {"title": title}

        channel = kwargs.get("channel")

        # 发送渠道
        if channel:
            params.update({"channel": channel})

        desp = kwargs.get("desp")

        # 消息内容
        if desp:
            params.update({"desp": desp})

        openid = kwargs.get("openid")

        if openid:
            params.update({"openid": openid})

        res = re.post(self.url, params=params).json()
        if res["code"] == 0:
            print("消息推送成功")
        else:
            print(f"推送错误, {res['info']}")
