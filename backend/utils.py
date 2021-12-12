# Comicker - Utils

from typing import (
    TYPE_CHECKING, TypeVar, Coroutine, Callable, Union, Optional, NoReturn,
    Iterable, Literal, Dict, Tuple, List
)

from sanic.response import HTTPResponse, json
from sanic.exceptions import SanicException
from sanic.errorpages import HTMLRenderer

from functools import partial, wraps
from ujson import dumps
from time import time

if TYPE_CHECKING:
    from . import Request


def api(
    message: str, data: Union[int, str, list, dict, None],
    status: int = 200, ensure_ascii: bool = True, **kwargs
) -> HTTPResponse:
    "API用のレスポンスを返します。"
    kwargs["dumps"] = partial(dumps, ensure_ascii=ensure_ascii)
    kwargs["status"] = status
    return json(
        {
            "status": kwargs["status"],
            "message": message,
            "data": data
        }, **kwargs
    )


DEFAULT_GET_REMOTE_ADDR = lambda request: request.ip
DEFAULT_COOLDOWN = "リクエストのしすぎです。"
GetRemoteAddress = Callable[["Request"], str]


class CoolDown:
    "細かくレート制限をRouteにかけたい際に使えるデコレータの名を持つクラスです。"

    rate: int
    per: float
    cache_max: int
    message: str
    strict: bool
    max_per: float
    cache: Dict[str, Tuple[int, float]]
    func: Callable[..., Coroutine]

    def __new__(
        cls, rate: int, per: float, message: str = DEFAULT_COOLDOWN, wrap_html: bool = False,
        cache_max: int = 1000, strict: bool = True, max_per: Optional[float] = None,
        get_remote_address: GetRemoteAddress = DEFAULT_GET_REMOTE_ADDR
    ) -> Callable[[Callable[..., Coroutine]], "CoolDown"]:
        self = super().__new__(cls)
        self.rate, self.per, self.strict = rate, per, strict
        self.cache_max, self.message = cache_max, message
        self.max_per = max_per or per * cache_max // 100
        self.cache, self.wrap_html = {}, wrap_html
        self.get_remote_address = get_remote_address

        def decorator(func):
            self.func = func
            return wraps(func)(self)

        return decorator

    async def _async_call(self, request, *args, **kwargs):
        ip = self.get_remote_address(request)
        before = self.cache.get(ip, (0, (now := time()) + self.per))
        self.cache[ip] = (
            before[0] + 1, before[1]
        )
        if self.cache[ip][1] > now:
            if self.cache[ip][0] > self.rate:
                if self.strict and self.cache[ip][1] < self.max_per:
                    self.cache[ip][1] += self.per
                e = SanicException(
                    self.message.format(self.cache[ip][1] - now), 429
                )
                if self.wrap_html:
                    return HTMLRenderer(request, e, True).full()
                else:
                    raise e
        else:
            del self.cache[ip]
        return await self.func(request, *args, **kwargs)

    def __call__(self, request: "Request", *args, **kwargs):
        # もしキャッシュが最大数になったのならcacheで一番古いものを削除する。
        if len(self.cache) >= self.cache_max:
            del self.cache[max(list(self.cache.items()), key=lambda _, d: d[1])[0]]
        # 非同期で実行できるようにコルーチン関数を返す。
        return self._async_call(request, *args, **kwargs)


MCFT = TypeVar("MCFT")
class MaxConcurrency:
    "最大同時実行数を設定します。"

    doing: Dict[str, List[Union[int, float]]]

    def __new__(
        cls, max_: int,
        get_remote_address: GetRemoteAddress = DEFAULT_GET_REMOTE_ADDR
    ) -> Callable[[MCFT], MCFT]:
        self = super().__new__(cls)
        self.max, self.get_remote_address = max_, get_remote_address
        self.doing = {}

        def decorator(func: MCFT):
            async def new(request, *args, **kwargs):
                self.check(request)
                ip = self.get_remote_address(request)
                try:
                    response = await func(request, *args, **kwargs)
                except Exception as e:
                    self.update(ip, "down")
                    raise e
                finally:
                    self.update(ip, "down")
                return response
            return wraps(func)(new)

        return decorator

    def update(
        self, ip: str, mode: Literal["up", "down"], default: Optional[list] = None
    ) -> None:
        "アクセス数をアップデートします。"
        if ip not in self.doing:
            self.doing[ip] = default or [0, time()]
        self.doing[ip][0] = self.doing[ip][0] + (1 if mode == "up" else -1)
        self.doing[ip][1] = time()
        if self.doing[ip][0] == 0:
            del self.doing[ip]

    def check(self, request: "Request") -> Union[None, NoReturn]:
        "実行できない場合はエラーを発生します。"
        ip = self.get_remote_address(request)
        now = self.doing.get(ip, [0, time()])
        if now[0] == self.max:
            raise SanicException(status_code=429)
        else:
            self.update(ip, "up", now)


def _add_cors_headers(response, methods: Iterable[str]) -> None:
    allow_methods = list(set(methods))
    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")
    headers = {
        "Access-Control-Allow-Methods": ",".join(allow_methods),
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": (
            "origin, content-type, accept, "
            "authorization, x-xsrf-token, x-request-id"
        ),
    }
    response.headers.extend(headers)


def add_cors_headers(request, response):
    if request and request.route and request.method != "OPTIONS":
        _add_cors_headers(response, [
            method
            for methods in request.route.methods
            for method in methods
        ])
 