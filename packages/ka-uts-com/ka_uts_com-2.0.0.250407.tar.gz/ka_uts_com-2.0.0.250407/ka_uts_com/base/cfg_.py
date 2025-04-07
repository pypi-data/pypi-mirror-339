# coding=utf-8
from typing import Any

from logging import Logger

from ka_uts_com.utils.pacmod import PacMod
from ka_uts_com.ioc.yaml_ import Yaml_

TyAny = Any
TyTimeStamp = int
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]
TyLogger = Logger


class Cfg_:
    """Configuration Class
    """
    sw_init: TyBool = False
    cfg: Any = None

    @classmethod
    def init(cls, com, **kwargs) -> None:
        if cls.sw_init:
            return
        cls.sw_init = True
        cls.cfg = Yaml_.read(PacMod.sh_path_cfg(com), com.Log)

    @classmethod
    def sh(cls, com, **kwargs) -> Any:
        if cls.sw_init:
            return cls
        cls.init(com, **kwargs)
        return cls.cfg
