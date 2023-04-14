from bilibili import BiliBili
from config import config
from push import PushSender, parse


def parse_message(message, push_type):
    if push_type == "pushplus":
        return parse(message, template="html")
    else:
        return parse(message, template="markdown")


def pushMessage(message, config):
    if isinstance(config, list):
        for item in config:
            t = item.get("type")

            p = PushSender(t, item.get("key"))

            p.send(parse_message(message, t), title="Bilibili")
    else:
        t = config.get("type")

        p = PushSender(config.get("type"), config.get("key"))

        p.send(parse_message(message, t), title="Bilibili")


def main(*args):
    accounts = config.get("multi")
    push_together = config.get("push")

    messages = []

    for item in accounts:
        obj = BiliBili(**item)

        res = obj.start()

        push = item.get("push")

        if push is None:
            if push_together is not None:
                messages.extend(res)
        else:
            pushMessage(res, push)

    if len(messages) != 0 and push_together is not None:
        pushMessage(messages, push_together)


if __name__ == "__main__":
    main()
