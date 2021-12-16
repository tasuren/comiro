# Comicker - API

from sanic import Blueprint

from aiohttp import ClientResponseError, InvalidURL
from urllib.parse import unquote

from .utils import api, MaxConcurrency, CoolDown
from . import Request


bp = Blueprint("API")


@bp.post("/set")
@MaxConcurrency(1)
@CoolDown(5, 30)
async def set_(request: Request):
    "新しく漫画を登録します。"
    try:
        return api(
            "Created", await request.app.ctx.data.set(unquote(request.body.decode())), 201
        )
    except ClientResponseError as e:
        return api(
            "Error", {
                "code": "connect", "status": e.status, "message": str(e)
            }, 400
        )
    except InvalidURL:
        return api("Error", {"code": "InvalidURL"}, 400)


@bp.route("/get", methods=("GET", "POST"))
@CoolDown(5, 5)
async def get(request: Request):
    "渡された複数のURLのデータを取得します。"
    return api(
        "OK", await request.app.ctx.data.get(
            list(map(
                unquote, request.body.decode().split(",- -,")
            ))
        )
    )


@bp.get("/search/<offset:int>/<word>")
@CoolDown(7, 5)
async def search(request: Request, offset: int, word: str):
    "検索を行います。"
    return api("OK", await request.app.ctx.data.search(word, offset))