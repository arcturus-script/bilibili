class dict2html:
    """
    字典转成 html
    """

    @staticmethod
    def link(*arg, **kwargs) -> str:
        """
        Parameter:
            可接收一个字典列表(List[Dict])作为位置参数, 如

            dict2html.link(
                [
                    {
                        "title": "1",
                        "url": "https://....",
                        "Class": "link",
                        "Style": "color: blue;",
                    },
                    {
                        "title": "2",
                        "url": "https://....",
                    },
                ],
            )

            也可以只接收关键词参数, 如

            dict2html.link(
                title="这是一个链接",
                url="https://....",
                Class="link",
                Style="color: blue;",
            )

        return:
            <a href='https://....' class='link' style='color: blue;'>这是一个链接</a>
        """
        if arg:
            Link = []
            for item in arg[0]:
                title = item.get("title")
                if title is None:
                    raise TypeError("link() missing 1 required argument: 'title'")

                url = item.get("url")
                if url is None:
                    raise TypeError("link() missing 1 required argument: 'url'")

                Class = item.get("Class")
                Style = item.get("Style")

                Link.append(f"<a href='{url}'")
                if Class:
                    Link.append(f"class='{Class}'")

                if Style:
                    Link.append(f"style='{Style}'")

                Link.append(f">{title}</a>")

            return " ".join(Link)
        else:
            title = kwargs.get("title")
            if title is None:
                raise TypeError("link() missing 1 required argument: 'title'")

            url = kwargs.get("url")
            if url is None:
                raise TypeError("link() missing 1 required argument: 'url'")

            Class = kwargs.get("Class")
            Style = kwargs.get("Style")

            Link = [f"<a href='{url}'"]
            if Class:
                Link.append(f"class='{Class}'")

            if Style:
                Link.append(f"style='{Style}'")

            Link.append(f">{title}</a>")

            return " ".join(Link)

    @staticmethod
    def img(*arg, **kwargs) -> str:
        """
        Parameter:
            可接收一个字典列表作为位置参数, 如

            dict2html.img(
                [
                    {
                        "alt": "1",
                        "url": "https://1.png",
                        "Class": "image",
                        "Style": "width: 100px;",
                    },
                    {
                        "alt": "2",
                        "url": "https://2.png",
                    },
                ],
            )

            可接收关键词参数, 如

            dict2html.img(
                url="http://..",
                Class="image",
                Style="width: 100px;",
            )

        return:
            <img src='https://1.png' alt='1' class='image' />
        """

        if arg:
            image = []
            for item in arg[0]:
                alt = item.get("alt", "image")

                url = item.get("url")
                if url is None:
                    raise TypeError("Dict missing 1 required argument: 'url'")

                Class = item.get("Class")
                Style = item.get("Style")

                image.append(f"<img src='{url}' alt='{alt}'")
                if Class:
                    image.append(f"class='{Class}'")

                if Style:
                    image.append(f"style='{Style}'")

                image.append("/>")

            return " ".join(image)
        else:
            alt = kwargs.get("alt", "image")

            url = kwargs.get("url")
            if url is None:
                raise TypeError("img() missing 1 required argument: 'url'")

            Class = kwargs.get("Class")
            Style = kwargs.get("Style")

            image = [f"<img src='{url}' alt='{alt}'"]
            if Class:
                image.append(f"class='{Class}'")

            if Style:
                image.append(f"style='{Style}'")

            image.append("/>")

            return " ".join(image)

    @staticmethod
    def h1(content: str, *arg, **kwargs) -> str:
        h = ["<h1"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            h.append(f"class='{Class}'")

        if Style:
            h.append(f"style='{Style}'")

        h.append(f">{content}</h1>")

        return " ".join(h)

    @staticmethod
    def h2(content: str, *arg, **kwargs) -> str:
        h = ["<h2"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            h.append(f"class='{Class}'")

        if Style:
            h.append(f"style='{Style}'")

        h.append(f">{content}</h2>")

        return " ".join(h)

    @staticmethod
    def h3(content: str, *arg, **kwargs) -> str:
        h = ["<h3"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            h.append(f"class='{Class}'")

        if Style:
            h.append(f"style='{Style}'")

        h.append(f">{content}</h3>")

        return " ".join(h)

    @staticmethod
    def h4(content: str, *arg, **kwargs) -> str:
        h = ["<h4"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            h.append(f"class='{Class}'")

        if Style:
            h.append(f"style='{Style}'")

        h.append(f">{content}</h4>")

        return " ".join(h)

    @staticmethod
    def h5(content: str, *arg, **kwargs) -> str:
        h = ["<h5"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            h.append(f"class='{Class}'")

        if Style:
            h.append(f"style='{Style}'")

        h.append(f">{content}</h5>")

        return " ".join(h)

    @staticmethod
    def h6(content: str, *arg, **kwargs) -> str:
        h = ["<h6"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            h.append(f"class='{Class}'")

        if Style:
            h.append(f"style='{Style}'")

        h.append(f">{content}</h6>")

        return " ".join(h)

    @staticmethod
    def txt(content: str, *arg, **kwargs) -> str:
        h = ["<p"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            h.append(f"class='{Class}'")

        if Style:
            h.append(f"style='{Style}'")

        h.append(f">{content}</p>")

        return " ".join(h)

    @staticmethod
    def bold(content: str, *arg, **kwargs) -> str:
        b = ["<strong"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            b.append(f"class='{Class}'")

        if Style:
            b.append(f"style='{Style}'")

        b.append(f">{content}</strong>")

        return " ".join(b)

    @staticmethod
    def italic(content: str, *arg, **kwargs) -> str:
        i = ["<i"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            i.append(f"class='{Class}'")

        if Style:
            i.append(f"style='{Style}'")

        i.append(f">{content}</i>")

        return " ".join(i)

    @staticmethod
    def strikethrough(content: str, *arg, **kwargs) -> str:
        d = ["<del"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            d.append(f"class='{Class}'")

        if Style:
            d.append(f"style='{Style}'")

        d.append(f">{content}</del>")

        return " ".join(d)

    @staticmethod
    def blockQuote(content: str, *arg, **kwargs) -> str:
        bq = ["<blockquote"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            bq.append(f"class='{Class}'")

        if Style:
            bq.append(f"style='{Style}'")

        bq.append(f">{content}</blockquote>")

        return " ".join(bq)

    @staticmethod
    def orderedList(
        list_,
        *arg,
        **kwargs,
    ) -> str:
        """
        接收一个字典列表, ol 的样式由关键词参数传入

        dict2html.orderedList(
            ["开发部", "测试部"],
            Class="ol",
            Style="color: blue;",
        )
        """
        ol = ["<ol"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            ol.append(f"class='{Class}'")

        if Style:
            ol.append(f"style='{Style}'")

        ol.append(">")

        for item in list_:
            ol.append(f"<li>{item}</li>")

        ol.append("</ol>")

        return "".join(ol)

    @staticmethod
    def unOrderedList(
        list_,
        *arg,
        **kwargs,
    ) -> str:
        """
        dict2html.unOrderedList(
            ["开发部", "测试部"],
            Class_="ul",
            Style="color: blue;",
        )
        """
        ul = ["<ul"]

        Class = kwargs.get("Class")
        Style = kwargs.get("Style")

        if Class:
            ul.append(f"class='{Class}'")

        if Style:
            ul.append(f"style='{Style}'")

        ul.append(">")

        for item in list_:
            ul.append(f"<li>{item}</li>")

        ul.append("</ul>")

        return "".join(ul)

    @staticmethod
    def taskList(
        list_,
        *arg,
        **kwargs,
    ) -> str:
        """
        Parameter:
            接收一个位置参数, 如

            dict2html.taskList(
                [
                    {"content": "跑100公里", "Class": "checkbox"},
                    {"content": "完成大作业", "complete": True},
                ],
            )

            complete: 布尔型, 不写默认未完成
        """
        tl = []
        for item in list_:
            completed = item.get("complete")
            content = item.get("content")
            Class = item.get("Class")
            Style = item.get("Style")

            tl.append("<input type='checkbox' disabled='true'")

            if Class:
                tl.append(f"class='{Class}'")

            if Style:
                tl.append(f"style='{Style}'")

            if completed:
                tl.append(f"checked='checked'>{content}</input>")
            else:
                tl.append(f">{content}</input>")

        return " ".join(tl)

    @staticmethod
    def table(list_, *arg, **kwargs) -> str:
        """
        将列表元组转换成表格

        Parameter:
            接收一个元组列表(List[Tuple])作为位置参数, 如
            dict2html.table(
                [
                    ("标题", "内容"),
                    ("1", "A"),
                    ("2", "B"),
                ],
                Style="border: 1px;",
                thStyle="padding: 1px;",
                tdStyle="padding: 1px;",
            )
        """
        Style = kwargs.get("Style")
        thStyle = kwargs.get("thStyle")
        tdStyle = kwargs.get("tdStyle")

        tb = ["<table"]

        if Style:
            tb.append(f"style='{Style}'")
        else:
            tb.append("style='width: 100%;border-collapse: collapse;'")

        tb.append("><tr>")

        # 表头
        for i in list_[0]:
            tb.append("<th")
            if thStyle:
                tb.append(f"style='{thStyle}'")
            else:
                tb.append("style='text-align: center;border: 1px solid #e6e6e6;background-color: #F5F5F5;'")

            tb.append(f">{i}</th>")

        tb.append("</tr>")

        # 表内容
        for item in list_[1:]:
            tb.append("<tr>")

            for i in item:
                tb.append(f"<td")
                if tdStyle:
                    tb.append(f"style='{tdStyle}'")
                else:
                    tb.append("style='text-align: center;border: 1px solid #e6e6e6;'")
                
                tb.append(f">{i}</td>")

            tb.append("</tr>")

        tb.append("</table>")

        return " ".join(tb)

    @staticmethod
    def dict2html(list_) -> str:
        """
        字典转成 html

        dict2html.dict2html(
            [
                {
                    "h1": {
                        "content": "标题1",
                        "params": {"Class": "h1"},
                    }
                },
                {
                    "txt": {
                        "content": "纯文本",
                        "params": {"Style": "font-size: 10px;"},
                    },
                },
                {
                    "table": {
                        "content": [
                            ("描述", "内容"),
                            ("1", "A"),
                        ],
                    },
                    "link": {
                        "params": {
                            "url": "https://....",
                            "title": "测试",
                        }
                    },
                },
                {
                    "img": {
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
                    c = value.get("content")
                    if c:
                        content.append(func[key](c, **params))
                    else:
                        content.append(func[key](**params))
            except AttributeError as aex:
                print(f"出现错误, 详情: {aex}")
            except KeyError as kex:
                print(f"出现错误, 无法格式化 {kex} 类型")

        html = "".join(content)
        return html


func = {
    "link": dict2html.link,
    "img": dict2html.img,
    "h1": dict2html.h1,
    "h2": dict2html.h2,
    "h3": dict2html.h3,
    "h4": dict2html.h4,
    "h5": dict2html.h5,
    "h6": dict2html.h6,
    "blod": dict2html.bold,
    "italic": dict2html.italic,
    "strikethrough": dict2html.strikethrough,
    "blockQuote": dict2html.blockQuote,
    "orderedList": dict2html.orderedList,
    "unOrderedList": dict2html.unOrderedList,
    "taskList": dict2html.taskList,
    "table": dict2html.table,
    "txt": dict2html.txt,
}
