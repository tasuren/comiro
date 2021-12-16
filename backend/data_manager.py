# Comicker - Data Manager

from typing import Optional, Sequence, List

from asyncio import AbstractEventLoop
from aiomysql import Pool

from warnings import filterwarnings
from ujson import dumps, loads

from . import extract, Comic


filterwarnings("ignore", module="aiomysql")


class DataManager:

    TABLES = ("Comics",)

    def __init__(self, pool: Pool, loop: AbstractEventLoop):
        self.pool = pool
        loop.create_task(self._prepare_table())

    async def _prepare_table(self):
        # テーブルを準備します。
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"""CREATE TABLE IF NOT EXISTS {self.TABLES[0]} (
                        Url TEXT, Title TEXT, Images JSON
                    );"""
                )

    async def set(self, url: str) -> Comic:
        "データベースに渡されたURLにある漫画の画像を追加します。"
        data = await extract(url)
        dumped = dumps(data["images"], ensure_ascii=True)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await self._get(cursor, url):
                    await cursor.execute(
                        f"""UPDATE {self.TABLES[0]} SET Title = %s, Images = %s
                            WHERE Url = %s;""",
                        (data["title"], dumped, url)
                    )
                else:
                    await cursor.execute(
                        f"INSERT INTO {self.TABLES[0]} VALUES (%s, %s, %s);",
                        (url, data["title"], dumped)
                    )
        del dumped
        return data

    def comic_from_json(self, row: Sequence) -> Optional[Comic]:
        "渡された行から漫画データを作ります。"
        if row:
            return {"url": row[0], "title": row[1], "images": loads(row[2])}

    async def _get(self, cursor, url):
        await cursor.execute(
            f"SELECT Url, Title, Images FROM {self.TABLES[0]} WHERE Url = %s;",
            (url,)
        )
        return await cursor.fetchone()

    async def get(self, urls: List[str]) -> List[Comic]:
        "渡されたURLの漫画データを取得します。"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                return list(filter(
                    lambda data: data is not None, [
                        self.comic_from_json(await self._get(cursor, url))
                        for url in urls if url
                    ]
                ))

    async def search(self, word: str, offset: int, limit: int = 10) -> List[Comic]:
        "検索を行います。"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"SELECT * FROM {self.TABLES[0]} WHERE word LIKE %s OFFSET %s LIMIT %s;",
                    (word, offset, limit)
                )
                return [
                    self.comic_from_json(row)
                    for row in await cursor.fetchall() if row
                ]