# Comicker Frontend

from browser import document, alert, window, html
from browser.local_storage import storage

from src.data_manager import DataManager, get_category
from src import components


data = DataManager()
if (url := document.query.getvalue("view")):
    for comic in data.comics:
        if comic["url"] == url:
            components.remove_loading("loading_first")
            del document["main"]
            document["sub"] <= html.H1(comic["title"] or comic["url"])
            document["sub"] <= html.A(
                "戻る", Class="btn btn-dark", href="/bookshelf.html"
            ) + html.H2("目次") + html.UL(
                html.A(html.LI(get_category(category)), href=f"#{category}")
                for category in comic["images"] if comic["images"][category]
            ) + html.HR()
            for category in comic["images"]:
                if comic["images"][category]:
                    document["sub"] <= html.H3(get_category(category), id=category)
                    for image in comic["images"][category]:
                        document["sub"] <= html.IMG(
                            src=image["url"], alt=image["alt"], Class="img-fluid"
                        ) + html.BR() + html.BR()
            break
    else:
        alert("データ取得に失敗しました。")
        window.location.href = "/"
elif (url := document.query.getvalue("url")):
    d = data.set(url)
    if "url" in d:
        url = f"/bookshelf.html?view={d['url']}"
    else:
        d = d["data"]
        if d["code"] == "InvalidURL":
            alert("URLが無効です。")
        else:
            alert(f"そのURLへのアクセスにてエラーが発生しました。\nメッセージ：{d['message']}")
        url = "/bookshelf.html"
    window.location.href = url
elif document.query.getvalue("clear", "none") == "data":
    def clear(event):
        del document["clear"]
        storage["urls"] = ""
        window.location.href = "/"

    del document["main"]
    document["sub"] <= html.H1("本棚データ削除")
    document["sub"] <= html.BUTTON("データを削除", id="clear", Class="btn btn-danger")
    document["clear"].bind("click", clear)
else:
    components.remove_loading("loading_first")
    document["main"] <= components.get_bookshelf(data.comics)


for close_btn in document.select(".btn-close-white"):
    close_btn.bind(
        "click", lambda event: (
            data.remove(event.target.id)
            or setattr(window.location, "href", "/bookshelf.html")
        )
    )   