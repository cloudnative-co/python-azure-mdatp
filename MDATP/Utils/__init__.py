from ..Exception import APIException
import io
import datetime
import urllib.request
from .schema import Schemas
from jsonschema import validate, ValidationError


def get_arguments(args: dict, keys: list = None, ignores: list = None):
    ret = {}
    for ky in args:
        if ky == "self":
            continue
        if keys is not None:
            if ky not in keys:
                continue
        if ignores is not None:
            if ky in ignores:
                continue
        if args[ky] is not None:
            if isinstance(args[ky], datetime.datetime):
                ret[ky] = int(args[ky].timestamp())
            else:
                ret[ky] = args[ky]
    return ret


def validation(f):
    def wrapper(*args, **kwargs):
        method_name = f.__qualname__
        schema = Schemas[method_name]
        try:
            _kwargs = get_arguments(kwargs)
            validate(_kwargs, schema)
        except ValidationError as e:
            raise e
        return f(*args, **kwargs)
    return wrapper
