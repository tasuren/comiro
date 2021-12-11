# Comicker - Typed

from types import SimpleNamespace

from sanic import Sanic
from sanic.request import Request
from aiomysql import Pool


class TypedContext(SimpleNamespace):
    pool: Pool
    auth: dict
    test: bool


class TypedSanic(Sanic):
    ctx: TypedContext


class TypedRequest(Request):
    app: TypedSanic