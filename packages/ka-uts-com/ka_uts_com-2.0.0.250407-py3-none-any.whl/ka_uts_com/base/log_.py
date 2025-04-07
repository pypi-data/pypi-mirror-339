# coding=utf-8
from collections.abc import Callable
from typing import Any

import os
import logging
import logging.config
from logging import Logger
from datetime import datetime
import psutil

# from ka_uts_com.com import Com
from ka_uts_com.ioc.jinja2_ import Jinja2_

TyAny = Any
TyCallable = Callable[..., Any]
TyDateTime = datetime
TyTimeStamp = int
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]
TyDir = str
TyPath = str
TyLogger = Logger

TnAny = None | Any
TnArr = None | TyArr
TnBool = None | bool
TnDic = None | TyDic
TnTimeStamp = None | TyTimeStamp
TnDateTime = None | TyDateTime


class Log_:

    sw_init: bool = False
    log: TyLogger = logging.getLogger('dummy_logger')
    username: str = psutil.Process().username()

    @classmethod
    def sh_dir_run(cls, com) -> TyDir:
        """Show run_dir
        """
        # print(f"sh_dir_run com.dir_dat = {com.dir_dat}")
        # print(f"sh_dir_run com.cmd = {com.cmd}")
        # print(f"sh_dir_run com.tenant = {com.tenant}")
        # print(f"sh_dir_run com = {com}")
        dir_dat: str = com.dir_dat
        tenant: str = com.tenant
        cmd: str = com.cmd
        package: str = com.d_app_pacmod['package']
        # module: str = com.d_app_pacmod['module']
        if tenant is not None:
            path = f"{dir_dat}/{tenant}/RUN/{package}"
        else:
            path = f"{dir_dat}/RUN/{package}"
        if com.log_type == "usr":
            path = f"{path}/{cls.username}"
        if cmd is not None:
            path = f"{path}/{cmd}"
        # print(f"sh_dir_run path = {path}")
        # print("==================================")
        return path

    @classmethod
    def sh_d_log_cfg(cls, com, **kwargs) -> TyDic:
        """Read log file path with jinja2
        """
        dir_run = cls.sh_dir_run(com)
        if kwargs.get('sw_single_dir_run', True):
            # print("---sw_single_dir_run = True --------------")
            dir_run_errs = f"{dir_run}/logs"
            dir_run_wrns = f"{dir_run}/logs"
            dir_run_infs = f"{dir_run}/logs"
            dir_run_logs = f"{dir_run}/logs"
            dir_run_debs = f"{dir_run}/logs"
            if kwargs.get('sw_mk_dir_run', True):
                os.makedirs(dir_run_logs, exist_ok=True)
        else:
            # print("---sw_single_dir_run = False -------------")
            dir_run_errs = f"{dir_run}/errs"
            dir_run_wrns = f"{dir_run}/wrns"
            dir_run_infs = f"{dir_run}/infs"
            dir_run_logs = f"{dir_run}/logs"
            dir_run_debs = f"{dir_run}/debs"
            if kwargs.get('sw_mk_dir_run', True):
                os.makedirs(dir_run_errs, exist_ok=True)
                os.makedirs(dir_run_wrns, exist_ok=True)
                os.makedirs(dir_run_infs, exist_ok=True)
                os.makedirs(dir_run_logs, exist_ok=True)
                os.makedirs(dir_run_debs, exist_ok=True)
        # path_log_cfg: TyPath = PacMod.sh_path_log_cfg(com)
        module = com.d_app_pacmod['module']
        # print(f"sh_d_log_cfg cls.path_log_cfg = {cls.path_log_cfg}")
        d_log_cfg: TyDic = Jinja2_.read(
                com.path_log_cfg, com.Log,
                dir_run_errs=dir_run_errs,
                dir_run_wrns=dir_run_wrns,
                dir_run_infs=dir_run_infs,
                dir_run_logs=dir_run_logs,
                dir_run_debs=dir_run_debs,
                module=module,
                pid=com.pid,
                ts=com.ts)
        # print(f"sh_d_log_cfg d_log_cfg = {d_log_cfg}")
        sw_debug: TyBool = kwargs.get('sw_debug', False)
        if sw_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        logger_name = com.log_type
        d_log_cfg['handlers'][f"{logger_name}_debug_console"]['level'] = level
        d_log_cfg['handlers'][f"{logger_name}_debug_file"]['level'] = level

        return d_log_cfg

    @classmethod
    def init(cls, com, **kwargs) -> None:
        """Set static variable log level in log configuration handlers
        """
        cls.sw_init = True
        d_log_cfg = cls.sh_d_log_cfg(com, **kwargs)
        logging.config.dictConfig(d_log_cfg)
        cls.log = logging.getLogger(com.log_type)

    @classmethod
    def sh(cls, com, **kwargs) -> TyLogger:
        if cls.sw_init:
            return cls.log
        cls.init(com, **kwargs)
        return cls.log
