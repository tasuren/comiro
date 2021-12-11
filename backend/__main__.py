# Comicker

from traceback import print_exc

from sanic.exceptions import SanicException

from asyncio import all_tasks
from ujson import load
from sys import argv

from .__init__ import Sanic, Request, logger
from .__init__.utils import api


app = Sanic("comicker")
app.ctx.test = argv[0] == "test"
with open("auth.json", "r") as f:
    app.ctx.auth = load(f)


@app.route("/ping")
async def ping(request: Request):
    return api(
        "pong", {
            "test": app.ctx.test, "pool": app.ctx.pool.size,
            "tasks": len(all_tasks())
        }
    )


@app.exception(Exception)
async def on_error(request: Request, exception: Exception):
    # 発生したエラーは辞書に直す。
    status = 200
    if isinstance(exception, SanicException):
        status = exception.status_code
        res = api(str(exception), None, exception.status_code)
    else:
        status = 500
        res = api(str(exception), None, 500)
        print_exc()

    if status in (500, 501):
        # もし内部エラーが発生したのならログを出力しておく。
        logger.error(f"Error on {request.path} : {exception}")

    return res


app.run()