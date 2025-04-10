import importlib
import sys
import typing
from types import GenericAlias, NoneType, UnionType
from typing import (
    ForwardRef,
    TypeVar,
    Union,
    _GenericAlias,
    get_args,
    get_origin,
)

from ovld import parametrized_class_check

UnionAlias = type(Union[int, str])


def clsstring(cls):
    cls = getattr(cls, "original_type", cls)
    if args := typing.get_args(cls):
        origin = typing.get_origin(cls) or cls
        args = ", ".join(map(clsstring, args))
        return f"{origin.__name__}[{args}]"
    else:
        r = repr(cls)
        if r.startswith("<class "):
            return cls.__name__
        else:
            return r


#################
# evaluate_hint #
#################


def evaluate_hint(typ, ctx=None, lcl=None, typesub=None):
    if isinstance(typ, str):
        if ctx is not None and not isinstance(ctx, dict):
            if isinstance(ctx, (GenericAlias, _GenericAlias)):
                origin = get_origin(ctx)
                if hasattr(origin, "__type_params__"):
                    subs = {p: arg for p, arg in zip(origin.__type_params__, get_args(ctx))}
                    typesub = {**subs, **(typesub or {})}
                ctx = origin
            if hasattr(ctx, "__type_params__"):
                lcl = {p.__name__: p for p in ctx.__type_params__}
            ctx = importlib.import_module(ctx.__module__).__dict__
        return evaluate_hint(eval(typ, ctx, lcl), ctx, lcl, typesub)

    elif isinstance(typ, (UnionType, GenericAlias, _GenericAlias)):
        origin = get_origin(typ)
        args = get_args(typ)
        if origin is UnionType:
            origin = Union
        new_args = [evaluate_hint(arg, ctx, lcl, typesub) for arg in args]
        return origin[tuple(new_args)]

    elif isinstance(typ, TypeVar):
        return typesub.get(typ, typ) if typesub else typ

    elif isinstance(typ, ForwardRef):
        if sys.version_info >= (3, 13):
            return typ._evaluate(ctx, lcl, type_params=None, recursive_guard=frozenset())
        else:  # pragma: no cover
            return typ._evaluate(ctx, lcl, recursive_guard=frozenset())

    elif isinstance(typ, type):
        return typ

    else:
        raise TypeError("Cannot evaluate hint:", typ, type(typ))


def _json_type_check(t, bound=object):
    origin = get_origin(t)
    if t is typing.Union:
        return all(_json_type_check(t2) for t2 in get_args(t))
    if not isinstance(origin or t, type) or not issubclass(origin or t, bound):
        return False
    if t in (int, float, str, bool, NoneType):
        return True
    if origin is list:
        (et,) = get_args(t)
        return _json_type_check(et)
    if origin is dict:
        kt, vt = get_args(t)
        return (kt is str) and _json_type_check(vt)
    return False


JSONType = parametrized_class_check(_json_type_check)
