# coding=utf-8
from typing import Any

from logging import Logger

from ka_uts_com.utils.pacmod import PacMod
from ka_uts_com.ioc.yaml_ import Yaml_

TyAny = Any
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]
TyLogger = Logger

TnAny = None | Any
TnArr = None | TyArr
TnBool = None | bool
TnDic = None | TyDic


class App_:
    """Aplication Class
    """
    sw_init: TyBool = False
    sw_replace_keys: TnBool = None
    keys: TnArr = None
    httpmod: TyAny = None
    reqs: TyDic = {}
    app: TyDic = {}

    @classmethod
    def init(cls, com, **kwargs) -> None:
        if cls.sw_init:
            return
        cls.sw_init = True
        cls.httpmod = kwargs.get('httpmod')
        cls.sw_replace_keys = kwargs.get('sw_replace_keys', False)
        if cls.sw_replace_keys:
            try:
                cls.keys = Yaml_.read(PacMod.sh_path_keys(com), com.Log)
            except Exception as exc:
                com.Log.error(exc, exc_info=True)
                raise

    @classmethod
    def sh(cls, com, **kwargs) -> Any:
        if cls.sw_init:
            return cls
        cls.init(com, **kwargs)
        return cls
