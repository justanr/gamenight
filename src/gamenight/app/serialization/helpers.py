from collections.abc import Mapping
from functools import partial, wraps
from typing import Any, Callable, Type, Union

from flask import jsonify
from flask.wrappers import Response
from marshmallow import Schema
from marshmallow.class_registry import get_class as get_schema


SCHEMA_LOOKUP_TYPE = Union[Type[Schema], Schema, str]


def _unpack_for_serialization(resp):
    if not isinstance(resp, tuple):
        return resp, None, None

    return (resp + (None, None))[:3]


def serialize_with(f=None, *, schema: SCHEMA_LOOKUP_TYPE, **kwargs):
    if f is None:
        return lambda f: serialize_with(f, schema=schema, **kwargs)

    if isinstance(schema, str):
        schema = get_schema(schema)

    @wraps(f)
    def wrapper(*a, **k):
        result = f(*a, **k)

        # already a fully realized response
        # we probably had to do something special
        # so pass it through despite this decorator
        # being applied
        if isinstance(result, Response):
            return result

        result, code, headers = _unpack_for_serialization(result)

        if not isinstance(schema, Schema):
            dumper = schema(**kwargs).dump
        else:
            dumper = schema.dump

        return jsonify(dumper(result).data), code, headers

    return wrapper
