# Comicker - Backend

from .typed import TypedSanic as Sanic, TypedRequest as Request
from .extractor import extract, Comic
from .data_manager import DataManager

from sanic.log import logger