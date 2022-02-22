import requests as re

class workWechatApp:
    """
    企业微信推送
    内部应用开发文档(https://work.weixin.qq.com/api/doc/90000/90135/90664)
    接口调试工具(https://open.work.weixin.qq.com/wwopen/devtool/interface/combine)
    相关参数获取方法(https://work.weixin.qq.com/api/doc/90000/90135/90665)
    """

    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    push_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

    def __init__(
        self,
        agentid: str,
        corpSecret: str,
        corpid: str,
    ) -> None:
        self.agentid = agentid
        self.corpSecret = corpSecret
        self.corid = corpid

    # 获取授权码
    def get_access_token(self) -> str or None:
        params = {"corpid": self.corid, "corpsecret": self.corpSecret}
        res = re.get(workWechatApp.token_url, params).json()
        if res.get("errcode") == 0:
            return res["access_token"]
        else:
            print(f"获取token出错, 详细信息:{res.get('errmsg')}")

    # 消息推送
    def push_msg(
        self,
        content: str,
        title: str,
        msgtype: str = "text",
        safe: int = 0,
        duplicate_check: int = 0,
        check_interval: int = 1800,
        **kwargs,
    ) -> None:
        """
        Parameters:
            msgtype: markdown and text
        """
        data = {
            "msgtype": msgtype,
            msgtype: {
                "content": f"{title}\n{content}",
            },
            "touser": kwargs.get("touser", "@all"),
            "toparty": kwargs.get("toparty", ""),
            "totag": kwargs.get("totag", ""),
            "agentid": self.agentid,
            "safe": safe,
            "enable_duplicate_check": duplicate_check,
            "duplicate_check_interval": check_interval,
        }

        access_token = self.get_access_token()
        res = re.post(
            workWechatApp.push_url,
            params={"access_token": access_token},
            json=data,
        ).json()

        errcode = res.get("errcode")
        if errcode == 0:
            print("消息发送成功")
        elif errcode == 81013:
            print("接收人无权限或不存在")
        elif errcode == 82001:
            print("touser & toparty & totag 不合法")
        else:
            print(f"消息发送失败, 详细原因: {res.get('errmsg')}")


class workWechatRobot:
    """
    企业微信群聊机器人
    配置说明(https://work.weixin.qq.com/api/doc/90000/90136/91770)
    """

    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"

    def __init__(self, key: str) -> None:
        self.key = key

    def push_msg(self, content: str, title: str, msgtype: str = "text") -> None:
        """
        Parameters:
            msgtype: markdown and text
        """
        res = re.post(
            workWechatRobot.webhook,
            params={"key": self.key},
            json={
                "msgtype": msgtype,
                msgtype: {
                    "content": f"{title}\n{content}",
                },
            },
        ).json()

        errcode = res.get("errcode")
        if errcode == 0:
            print("机器人发送消息成功")
        elif errcode == 93000:
            print("机器人的key错误")
        else:
            print(f"消息推送错误, 详细原因: {res.get('errmsg')}")
