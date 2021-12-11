# Comicker - Typed

from typing import TYPE_CHECKING
from types import SimpleNamespace

from sanic import Sanic
from sanic.request import Request
from aiomysql import Pool

if TYPE_CHECKING:
    from . import DataManager


class TypedContext(SimpleNamespace):
    pool: Pool
    auth: dict
    test: bool
    data: "DataManager"


class TypedSanic(Sanic):
    ctx: TypedContext


class TypedRequest(Request):
    app: TypedSanic