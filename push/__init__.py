from .workWeChat import workWechatRobot, workWechatApp
from .server import server
from .qmsg import qmsg
from .pushplus import pushplus

import os

from .tools.dict2html import dict2html
from .tools.dict2md import dict2md
from .tools.dict2text import dict2text


def push(type: str, title: str, content):
    try:
        if type == "pushplus":
            try:
                key = os.environ["pushplus"]

                # 这里暂时只推送 html
                res = pushplus(key).push_msg(
                    dict2html.dict2html(content),
                    title=title,
                    template="html",
                )

                print(res)
            except KeyError:
                print("未配置 pushplus 的 token")
        elif type == "server":
            try:
                key = os.environ["server"]

                # 这里推送 markdown
                res = server(key).push_msg(
                    desp=dict2md.dict2md(content),
                    title=title,
                )
            except KeyError:
                print("未配置 server 酱 的 key")
        elif type == "workWechatRobot":
            try:
                key = os.environ["workWechatRobot"]

                # 这里推送 text(当然也可以推送 markdown, 但是微信不支持)
                res = workWechatRobot(key).push_msg(
                    title=title,
                    content=dict2text.dict2text(content),
                )
            except KeyError:
                print("未配置微信机器人的 key")
        elif type == "workWechat":
            try:
                print(dict2text.dict2text(content))
                
                agentid = os.environ["agentid"]
                corpSecret = os.environ["corpSecret"]
                corid = os.environ["corpid"]
                
                # 这里推送 text(当然也可以推送 markdown, 但是微信不支持)
                res = workWechatApp(agentid, corpSecret, corid).push_msg(
                    title=title,
                    content=dict2text.dict2text(content),
                )
            except KeyError as key:
                print(f"未配置企业微信的 {key}")
        #qmsg推送
        elif type == "qmsg":
            try:
                key = os.environ["qmsg"]
                # 这里推送文本消息
                res = qmsg(key).push_msg(dict2md.dict2md(content))
            except KeyError:
                print("未配置 qmsg 酱 的 key")
        else:
            print("未找到相关推送服务")
    except Exception as ex:
        print(f"推送时发生错误, 详情: {ex}")
