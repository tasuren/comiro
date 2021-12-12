# Comicker Frontend

from browser import document, alert, window

from src.data_manager import DataManager, Error
from src import components


data = DataManager()
if (url := document.query.getvalue("view")):
    for comic in data.comics:
        if comic["url"] == url:
            components.remove_loading("loading_first")
            break
    else:
        alert("データ取得に失敗しました。")
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
else:
    components.remove_loading("loading_first")
    document["main"] <= components.get_bookshelf(data.comics)