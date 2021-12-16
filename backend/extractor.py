# Comicker - Extractor

from typing import TypedDict, Optional, DefaultDict, Tuple, List

from collections import defaultdict
from aiohttp import ClientSession
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53"
}
class ImageData(TypedDict):
    alt: str
    url: str
class Comic(TypedDict):
    images: DefaultDict[str, List[ImageData]]
    title: str
    url: str


async def extract(url: str, headers: Optional[dict] = None) -> Comic:
    "渡されたURLにある画像を取り出します。"
    async with ClientSession() as session:
        async with session.get(url, headers=headers or HEADERS) as r:
            r.raise_for_status()
            soup = BeautifulSoup(await r.text(), "html.parser")
    images = defaultdict(list)
    for img in soup.find_all("img"):
        if img.get("src"):
            images[img.get("class", ("__nothing__",))[0]].append(
                {"alt": img.get("alt", img["src"]), "url": img["src"]}
            )
    title = soup.find("title")
    return {"title": title.text if title else url, "images": images, "url": url}


if __name__ == "__main__":
    from asyncio import run

    data = run(extract("https://eromanga-yoru.com/jk-jc/283899"))
    print(data["title"])
    for class_, images in data["images"].items():
        print(f"{class_}")
        for image in images:
            print(f"\t{image['alt']}, {image['url']}")