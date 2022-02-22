class dict2text:
    """
    将字典转成 text
    """

    @staticmethod
    def txt(content: str, newline: str = "\n") -> str:
        return f"{content}{newline}"

    @staticmethod
    def orderedList(list_, newline="\n") -> str:
        content = []
        for index, value in enumerate(list_):
            content.append(f"{index+1}. {value}{newline}")

        return "".join(content)

    @staticmethod
    def unOrderedList(list_, newline="\n") -> str:
        content = []
        for value in list_:
            content.append(f"· {value+1}{newline}")

        return "".join(content)

    @staticmethod
    def taskList(list_, newline="\n") -> str:
        """
        Parameter:
            接收一个位置参数, 如
            dict2md.taskList(
                [
                    {"content": "跑100公里"},
                    {"content": "完成大作业", "complete": True},
                ],
            )

            complete: 布尔型, 不写默认未完成

        return:
            [ ] 跑100公里
            [x] 完成大作业
        """
        content = []
        for dict_ in list_:
            completed = dict_.get("complete")
            if completed:
                content.append(f"[x] {dict_.get('content')}{newline}")
            else:
                content.append(f"[ ] {dict_.get('content')}{newline}")

        return "".join(content)

    @staticmethod
    def table(list_, *, newline: str = "\n", **kwargs) -> str:
        """
        Parameter:
            接收一个元组列表作为位置参数, 如
            dict2md.table(
                [
                    ("标题", "内容"),
                    ("1", "A"),
                    ("2", "B"),
                ],
                newline="\n",
            )

            关键词参数
            newline: 换行符, 选填, 默认 \n

        return:
            1: 内容1(A) 内容2(AA)
            2: 内容1(B) 内容2(BB)
        """
        content = []
        t = list_[0][1:]

        # 表内容
        for tuple_ in list_[1:]:
            content.append(f"{tuple_[0]}: ")
            for index, value in enumerate(tuple_[1:]):
                content.append(f"{t[index]}({value}) ")
            content.append(f"{newline}")

        return "".join(content)

    @staticmethod
    def dict2text(list_, newline="\n") -> str:
        """
        将字典列表转成 text

        Parameter:
            接收一个字典列表, 键对映于静态方法名, 字典项可包含多个键

            dict2text.dict2text(
                [
                    {
                        "h1": {
                            "content": "标题1",
                        }
                    },
                    {
                        "orderedList": {
                            "content": ["hello", "hi"],
                        }
                    },
                    {
                        "txt": {"content": "纯文本"},
                    },
                    {
                        "table": {
                            "params": {"position": "center", "newline": "\n"},
                            "content": [
                                ("描述", "内容1", "内容2"),
                                ("1", "A", "AA"),
                                ("2", "B", "BB"),
                            ],
                        },
                        "taskList": {
                            "content": [
                                {"content": "跑100公里"},
                                {"content": "完成大作业", "complete": True},
                            ],
                        },
                    },
                ]
            )
        """
        content = []

        for dict_ in list_:
            try:
                for key, value in dict_.items():
                    # 接收关键词参数
                    params = value.get("params", {})

                    # 这里使用 newline 参数覆盖 params 里的换行符
                    params.update({"newline": newline})

                    c = value.get("content")
                    if c:
                        content.append(func[key](c, **params))
                    else:
                        content.append(func[key](**params))
            except AttributeError as aex:
                print(f"出现错误, 详情: {aex}")
            except KeyError as kex:
                print(f"出现错误, 无法格式化 {kex} 类型")

        return "".join(content)


# 类静态方法列表
func = {
    "h1": dict2text.txt,
    "h2": dict2text.txt,
    "h3": dict2text.txt,
    "h4": dict2text.txt,
    "h5": dict2text.txt,
    "h6": dict2text.txt,
    "blod": dict2text.txt,
    "italic": dict2text.txt,
    "strikethrough": dict2text.txt,
    "blockQuote": dict2text.txt,
    "orderedList": dict2text.orderedList,
    "unOrderedList": dict2text.unOrderedList,
    "taskList": dict2text.taskList,
    "table": dict2text.table,
    "txt": dict2text.txt,
}
