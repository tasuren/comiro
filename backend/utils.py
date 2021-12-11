# Comicker - Utils

from typing import Union

from sanic import response

from functools import partial
from ujson import dumps


def api(
    message: str, data: Union[int, str, list, dict, None],
    status: int = 200, ensure_ascii: bool = True, **kwargs
) -> response.HTTPResponse:
    "API用のレスポンスを返します。"
    kwargs["dumps"] = partial(dumps, ensure_ascii=ensure_ascii)
    kwargs["status"] = status
    return response.json(
        {
            "status": kwargs["status"],
            "message": message,
            "data": data
        }, **kwargs
    )