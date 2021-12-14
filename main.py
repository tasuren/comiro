# Comicker

from sanic.exceptions import SanicException
from aiomysql import create_pool

from asyncio import all_tasks, AbstractEventLoop
from traceback import print_exc
from ujson import load
from sys import argv

from backend import Sanic, Request, logger, DataManager
from backend.utils import api, add_cors_headers

from backend.api import bp as api_bp


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


@app.listener("before_server_start")
async def before_server_start(app: Sanic, loop: AbstractEventLoop):
    app.ctx.pool = await create_pool(1, 1000, loop=loop, **app.ctx.auth["mysql"])
    app.ctx.data = DataManager(app.ctx.pool, loop)


@app.listener("after_server_stop")
async def after_server_stop(app: Sanic, _: AbstractEventLoop):
    app.ctx.pool.close()
    await app.ctx.pool.wait_closed()


@app.exception(Exception)
async def on_error(request: Request, exception: Exception):
    # 発生したエラーは辞書に直す。
    status = 200
    name = f"{exception.__class__.__name__}: {exception}"
    if isinstance(exception, SanicException):
        status = exception.status_code
        res = api("Error", name, exception.status_code)
    else:
        status = 500
        res = api("Error", name, 500)
        print_exc()

    if status in (500, 501):
        # もし内部エラーが発生したのならログを出力しておく。
        logger.error(f"Error on {request.path} : {exception}")

    return res


app.blueprint(api_bp)
app.register_middleware(add_cors_headers, "response")


app.run(**app.ctx.auth["app"])