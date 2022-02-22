import requests as re


class pushplus:
    """
    推送加(https://www.pushplus.plus/)
    """

    push_url = "http://www.pushplus.plus/send"
    params_tuple = ("title", "channel", "topic", "webhook", "template")

    def __init__(self, token):
        self.token = token

    def push_msg(self, content, **kwargs):
        """
        消息推送方法

        使用 push_msg("测试", template="markdown", title="这是一个测试消息")
        """
        try:
            params = {
                "token": self.token,
                "content": content,
            }

            for keys, values in kwargs.items():
                if keys in pushplus.params_tuple:
                    params.update({keys: values})

            res = re.post(
                pushplus.push_url,
                json=params,
            ).json()

            if res.get("code") == 200:
                return "发送消息成功"
            else:
                return f"发送消息失败, 因为: {res.get('msg')}"
        except Exception as e:
            return f"推送时出现错误, 原因: {e}"