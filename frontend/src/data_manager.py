# Comicker Frontend - Data Manager

from browser.local_storage import storage
from browser import ajax, alert

from json import loads, dumps

from src.constants import URL


def get(urls, callback, **kwargs):
    ajax.post(
        f"{URL}/get", mode="json", data=",- -,".join(urls),
        oncomplete=callback, **kwargs
    )


def set_(url, callback, **kwargs):
    ajax.post(
        f"{URL}/set", data=url, oncomplete=callback, **kwargs
    )


class DataManager:
    def __init__(self):
        self.urls = [
            url for url in loads(storage.get("urls", "[]"))
        ]
        self.comics = []
        def on_load(response):
            data = response.json
            if data["status"] == 500:
                alert(
                    "エラーが発生しました。\n"
                    "もしこれが何度も表示され異常だと思った場合は、クレジットページにあるメールまたはDiscordから報告してください。\n"
                    f"また、もしかしたらデータ消去で治る可能性もあります。\nコード：{data}"
                )
            else:
                for comic in data["data"]:
                    self.comics.append(comic)
        get(self.urls, on_load, blocking=True)

    def set_comic(self, response):
        data = response.json
        if data["message"] == "Error":
            self.comics.append(data)
        else:
            data = data["data"]
            for index in range(len(self.comics)):
                if self.comics[index]["url"] == data["url"]:
                    del self.comics[index]
            self.comics.append(data)

    def set(self, url):
        set_(url, self.set_comic, blocking=True)
        data = self.comics[-1]
        if "url" in data:
            if url not in self.urls:
                self.urls.append(url)
                self.save()
        else:
            del self.comics[-1]
        return data

    def remove(self, url):
        if url in self.urls:
            self.urls.remove(url)
        if url in storage["urls"]:
            self.save()

    def save(self):
        storage["urls"] = dumps(self.urls)


def get_category(category):
    return "未分類" if category == "__nothing__" else category