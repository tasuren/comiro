# Comicker Frontend - Data Manager

from browser.local_storage import storage
from browser import ajax

from json import loads, dumps

from src.constants import URL


def get(urls, callback, **kwargs):
    ajax.get(
        f"{URL}/get", mode="json", data=",- -,".join(urls),
        oncomplete=callback, **kwargs
    )


def set_(url, callback, **kwargs):
    ajax.post(
        f"{URL}/set", data=url, oncomplete=callback, **kwargs
    )


class Error(Exception):
    ...


class DataManager:
    def __init__(self):
        self.urls = [
            url for url in loads(storage.get("urls", "[]"))
        ]
        self.comics = []
        def on_load(response):
            for comic in response.json:
                self.comics.append(comic)
        get(self.urls, on_load, blocking=True)

    def set_comic(self, response):
        data = response.json
        if data["message"] == "Error":
            self.comics.append(data)
        else:
            for index in range(len(self.comics)):
                if self.comics[index]["url"] == data["url"]:
                    del self.comics[index]
            self.comics.append(data)

    def set(self, url):
        if url not in self.urls:
            self.urls.append(url)
            self.save()
        set_(url, self.set_comic, blocking=True)
        data = self.comics[-1]
        if "url" not in self.comics:
            del self.comics[-1]
        return data

    def remove(self, url):
        if url in self.urls:
            self.urls.remove(url)
        if url in storage["urls"]:
            self.save()

    def save(self):
        storage["urls"] = dumps(self.urls)