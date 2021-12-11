# Comicker - API

from sanic import Blueprint

from aiohttp import ClientResponseError

from .utils import api, MaxConcurrency, CoolDown
from . import Request


bp = Blueprint("API")


@bp.route("/set")
@MaxConcurrency(1)
@CoolDown(5, 30)
async def set_(request: Request):
    "新しく漫画を登録します。"
    try:
        return api("Created", await request.app.ctx.data.set(request.body), 201)
    except ClientResponseError as e:
        return api("Error", {"status": e.status, "message": str(e)}, 400)


@bp.route("/get")
@CoolDown(5, 5)
async def get(request: Request):
    "渡された複数のURLのデータを取得します。"
    return api("OK", await request.app.ctx.data.get(request.json))


@bp.route("/search/<offset:int>/<word>")
@CoolDown(7, 5)
async def search(request: Request, offset: int, word: str):
    "検索を行います。"
    return api("OK", await request.app.ctx.data.search(word, offset))