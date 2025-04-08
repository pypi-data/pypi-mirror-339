# coding=utf-8
from collections.abc import Callable
from typing import Any

TyArr = list[Any]
TyCallable = Callable[..., Any]
TyDic = dict[Any, Any]
TyArrDic = TyArr | TyDic
TyDoC = dict[str, TyCallable]
TyMsg = str

TnStr = None | str
TnDoC = None | TyDoC
TnCallable = None | TyCallable


class Fnc:
    """
    Functions
    """
    @staticmethod
    def identity(obj: Any) -> Any:
        return obj

    @staticmethod
    def sh(doc: TnDoC, key: TnStr) -> TyCallable:
        if not doc:
            msg = f"function table: {doc} is not defined"
            raise Exception(msg)
        if not key:
            msg = f"key: {key} is not defined"
            raise Exception(msg)
        fnc: TnCallable = doc.get(key)
        if not fnc:
            msg = f"key: {key} is not defined in function table: {doc}"
            raise Exception(msg)
        return fnc

    @classmethod
    def ex(cls, doc: TnDoC, key: TnStr, args_kwargs: TyArrDic) -> Any:
        fnc: TyCallable = cls.sh(doc, key)
        return fnc(args_kwargs)
