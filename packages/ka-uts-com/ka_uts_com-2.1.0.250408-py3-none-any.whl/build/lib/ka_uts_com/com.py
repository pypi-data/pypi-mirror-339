# coding=utf-8
from typing import Any

import os
import time
import calendar
import logging
import logging.config
from logging import Logger
from datetime import datetime

from ka_uts_com.utils.aoeqstmt import AoEqStmt
from ka_uts_com.utils.pac import Pac
from ka_uts_com.utils.pacmod import PacMod
from ka_uts_com.base.app_ import App_
from ka_uts_com.base.cfg_ import Cfg_
from ka_uts_com.base.exit_ import Exit_
from ka_uts_com.base.log_ import Log_

TyAny = Any
TyDateTime = datetime
TyTimeStamp = int
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]
TyLogger = Logger

TnAny = None | Any
TnArr = None | TyArr
TnDic = None | TyDic
TnTimeStamp = None | TyTimeStamp
TnDateTime = None | TyDateTime
TnStr = None | str


class Com:
    """Communication Class
    """
    sw_init: bool = False
    dir_dat: TnStr = None
    tenant: TnStr = None
    log_type: TnStr = None
    cmd: TnStr = None
    d_com_pacmod: TyDic = {}
    d_app_pacmod: TyDic = {}
    path_bin = None
    path_log_cfg = None

    pid = None

    ts: TnTimeStamp
    ts_start: TnDateTime = None
    ts_end: TnDateTime = None
    ts_etime: TnDateTime = None
    d_timer: TyDic = {}

    cfg: TnDic = None
    Log = logging.getLogger('dummy_logger')
    App: Any = None
    Exit: Any = None

    @classmethod
    def init(cls, app_cls, kwargs: TyDic):
        """ set log and application (module) configuration
        """
        if cls.sw_init:
            return
        cls.sw_init = True
        cls.dir_dat = kwargs.get('dir_dat', '/data')
        cls.tenant = kwargs.get('tenant')
        cls.log_type = kwargs.get('log_type', 'std')
        cls.cmd = kwargs.get('cmd')
        cls.d_com_pacmod = PacMod.sh_d_pacmod(cls)
        cls.d_app_pacmod = PacMod.sh_d_pacmod(app_cls)
        cls.ts = calendar.timegm(time.gmtime())
        cls.pid = os.getpid()

        cls.path_bin = cls.sh_path_bin()
        cls.path_log_cfg = cls.sh_path_log_cfg()

        cls.Log = Log_.sh(cls, **kwargs)
        cls.cfg = Cfg_.sh(cls, **kwargs)
        cls.App = App_.sh(cls, **kwargs)
        cls.Exit = Exit_.sh(**kwargs)

    @classmethod
    def sh_kwargs(cls, app_cls, d_parms, *args) -> TyDic:
        _kwargs: TyDic = AoEqStmt.sh_d_eq(*args, d_parms=d_parms)
        cls.init(app_cls, _kwargs)
        _kwargs['com'] = cls
        return _kwargs

    @classmethod
    def sh_path_bin(cls) -> Any:
        """ show directory
        """
        package = cls.d_app_pacmod['package']
        path = "bin"
        return Pac.sh_path_by_package(package, path)

    @classmethod
    def sh_path_log_cfg(cls) -> Any:
        """ show directory
        """
        _packages = [cls.d_app_pacmod['package'], cls.d_com_pacmod['package']]
        _path = f"data/log.{cls.log_type}.yml"
        return Pac.sh_path_by_packages(_packages, _path)

    @classmethod
    def sh_path_cfg(cls) -> Any:
        """ show directory
        """
        package = cls.d_app_pacmod['package']
        path = 'data/cfg.yml'
        return Pac.sh_path_by_package(package, path)
