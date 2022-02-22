class dict2md:
    """
    将字典转成 markdown
    """

    @staticmethod
    def link(*args, newline: str = "\n", **kwargs) -> str:
        """
        Parameter:
            可接收一个字典列表作为位置参数, 如
            dict2md.link(
                [
                    {"title": "1", "url": "https://...."},
                    {"title": "2", "url": "https://...."},
                ],
            )

            也可以接收关键词参数, 如

            dict2md.link(title="1", "url"="https://....")

            title: 关键词参数
            url: 关键词参数
            newline: 关键词参数, 换行符, 选填

            有关键词参数则忽略位置参数

        return:
            [1](https://....)
            [2](https://....)
        """
        if args:  # 如果存在字典列表
            link_ = []
            for item in args[0]:
                title = item.get("title")
                if title is None:
                    raise TypeError("link() missing 1 required argument: 'title'")

                url = item.get("url")
                if url is None:
                    raise TypeError("link() missing 1 required argument: 'url'")

                link_.append(f"[{title}]({url}){newline}")

            return "".join(link_)
        else:
            title = kwargs.get("title")
            if title is None:
                raise TypeError("link() missing 1 required argument: 'title'")

            url = kwargs.get("url")
            if url is None:
                raise TypeError("link() missing 1 required argument: 'url'")

            return f"[{title}]({url}){newline}"

    @staticmethod
    def img(*args, newline: str = "\n", **kwargs) -> str:
        """
        Parameter:
            可接收一个字典列表作为位置参数, 如
            dict2md.img(
                [
                    {"alt": "1", "url": "https://1.png"},
                    {"alt": "2", "url": "https://2.png"},
                ],
                newline = "\n",
            )

            也可以接受关键词参数, 如
            dict2md.link(alt="1", "url"="https://1.png", newline="\n")

            alt: 关键词参数, 默认 image
            url: 关键词参数
            newline: 关键词参数, 换行符, 选填, 默认 \n

        return:
            ![1](https://1.png)
            ![2](https://2.png)
        """
        if args:
            img_ = []
            for item in args[0]:
                alt = item.get("alt")
                if alt is None:
                    alt = "image"

                url = item.get("url")
                if url is None:
                    raise TypeError("Dict missing 1 required argument: 'url'")

                img_.append(f"![{alt}]({url}){newline}")

            return "".join(img_)
        else:
            alt = kwargs.get("alt")
            if alt is None:
                alt = "image"

            url = kwargs.get("url")
            if url is None:
                raise TypeError("img() missing 1 required argument: 'url'")

            return f"![{alt}]({url}){newline}"

    @staticmethod
    def h1(content: str, newline: str = "\n") -> str:
        return f"# {content}{newline}"

    @staticmethod
    def h2(content: str, newline: str = "\n") -> str:
        return f"## {content}{newline}"

    @staticmethod
    def h3(content: str, newline: str = "\n") -> str:
        return f"### {content}{newline}"

    @staticmethod
    def h4(content: str, newline: str = "\n") -> str:
        return f"#### {content}{newline}"

    @staticmethod
    def h5(content: str, newline: str = "\n") -> str:
        return f"##### {content}{newline}"

    @staticmethod
    def h6(content: str, newline: str = "\n") -> str:
        return f"###### {content}{newline}"

    @staticmethod
    def txt(content: str, newline: str = "\n") -> str:
        return f"{content}{newline}"

    @staticmethod
    def bold(content: str) -> str:
        return f"**{content}**"

    @staticmethod
    def italic(content: str) -> str:
        return f"*{content}*"

    @staticmethod
    def strikethrough(content: str) -> str:
        return f"~~{content}~~"

    @staticmethod
    def blockQuote(content: str) -> str:
        return f"> {content}"

    @staticmethod
    def orderedList(list_, newline="\n") -> str:
        content = []
        for index, value in enumerate(list_):
            content.append(f"{index}. {value}{newline}")

        return "".join(content)

    @staticmethod
    def unOrderedList(list_, newline="\n") -> str:
        content = []
        for value in list_:
            content.append(f"- {value}{newline}")

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
            - [ ] 跑100公里
            - [x] 完成大作业
        """
        content = []
        for dict_ in list_:
            completed = dict_.get("complete")
            if completed:
                content.append(f"- [x] {dict_.get('content')}{newline}")
            else:
                content.append(f"- [ ] {dict_.get('content')}{newline}")

        return "".join(content)

    @staticmethod
    def table(list_, *, position: str = "center", newline: str = "\n") -> str:
        """
        Parameter:
            接收一个元组列表作为位置参数, 如
            dict2md.table(
                [
                    ("标题", "内容"),
                    ("1", "A"),
                    ("2", "B"),
                ],
                position="left",
                newline="\n",
            )

            关键词参数
            style: 表格风格, left 居左, center 居右, right 居右, 选填, 默认居中
            newline: 换行符, 选填, 默认 \n

        return:
            |标题|内容|
            |:--|:--|
            |1|A|
            |2|B|
        """
        content = ["\n"] # 这里在表格前面多加一个换行, 解决 pushplus 排版问题

        # 表头
        for i in list_[0]:
            content.append(f"|{i}")

        content.append(f"|{newline}")

        # 表格风格
        if position == "center":
            s = ":--:"
        elif position == "left":
            s = ":--"
        else:
            s = "--:"

        for _ in range(len(list_[0])):
            content.append(f"|{s}")
        content.append(f"|{newline}")

        # 表内容
        for tuple_ in list_[1:]:
            for i in tuple_:
                content.append(f"|{i}")
            content.append(f"|{newline}")

        return "".join(content) + "\n"  # 这里末尾也加上换行, 解决多账号排版

    @staticmethod
    def code(content: str, newline="\n") -> str:
        return f"`{content}`{newline}"

    @staticmethod
    def dict2md(list_, newline="\n") -> str:
        """
        将字典列表转成 markdown 语法

        Parameter:
            接收一个字典列表, 键对映于静态方法名, 字典项可包含多个键
            params 用于设置关键词参数

            dict2md.dict2md(
                [
                    {
                        "h1": {
                            "content": "标题1",
                        }
                    },
                    {
                        "txt": {"content": "纯文本"},
                    },
                    {
                        "table": {
                            "params": {"position": "center", "newline": "\n"},
                            "content": [
                                ("描述", "内容"),
                                ("1", "A"),
                            ],
                        },
                        "link": {
                            "params": {
                                "url": "https://....",
                                "title": "测试",
                                "newline": "\n",
                            }
                        },
                    },
                    {
                        "img": {
                            "params": {"newline": "\n"},
                            "content": [
                                {"url": "https://a.png"},
                            ],
                        }
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
    "link": dict2md.link,
    "img": dict2md.img,
    "h1": dict2md.h1,
    "h2": dict2md.h2,
    "h3": dict2md.h3,
    "h4": dict2md.h4,
    "h5": dict2md.h5,
    "h6": dict2md.h6,
    "blod": dict2md.bold,
    "italic": dict2md.italic,
    "strikethrough": dict2md.strikethrough,
    "blockQuote": dict2md.blockQuote,
    "orderedList": dict2md.orderedList,
    "unOrderedList": dict2md.unOrderedList,
    "taskList": dict2md.taskList,
    "table": dict2md.table,
    "txt": dict2md.txt,
    "code": dict2md.code,
}
