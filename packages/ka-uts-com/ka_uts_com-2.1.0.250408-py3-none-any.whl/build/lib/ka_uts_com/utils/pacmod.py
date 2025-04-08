# coding=utf-8
from typing import Any

from os import path as os_path

from ka_uts_com.utils.pac import Pac

TyArr = list[Any]
TyDic = dict[Any, Any]
TyPath = str


class PacMod:
    """ Package Module Management
    """
    @staticmethod
    def sh_d_pacmod(cls) -> TyDic:
        """ Show Pacmod Dictionary
        """
        a_pacmod: TyArr = cls.__module__.split(".")
        return {'package': a_pacmod[0], 'module': a_pacmod[1]}

    @staticmethod
    def sh_path_module_yaml(d_pacmod: TyDic) -> Any:
        """ show directory
        """
        package = d_pacmod['package']
        module = d_pacmod['module']
        path = f"{module}/data/{module}.yml"
        return Pac.sh_path_by_package(package, path)

    @staticmethod
    def sh_path_keys(d_pacmod: TyDic) -> Any:
        """ show directory
        """
        package = d_pacmod['package']
        path = 'data/keys.yml'
        return Pac.sh_path_by_package(package, path)

    # @staticmethod
    # def sh_path_log_cfg(com) -> TyPath:
    #     """ show directory
    #     """
    #     package = com.d_app_pacmod['package']
    #     path = resources.files(package).joinpath(f"data/log.{com.log_type}.yml")
    #     if path.is_file():
    #         return path
    #     package = com.d_com_pacmod['package']
    #     path = resources.files(package).joinpath(f"data/log.{com.log_type}.yml")
    #     if path.is_file():
    #         return path
    #     raise ModuleNotFoundError

    # @staticmethod
    # def sh_path_cfg(d_pacmod: TyDic) -> Any:
    #     """ show directory
    #     """
    #     package = com.d_app_pacmod['package']
    #     path = 'dat/cfg.yml'
    #     return Pac.sh_path(package, path)

    # @staticmethod
    # def sh_path_type(d_pacmod: TyDic, type_: str) -> str:
    #     """ show Data File Path
    #     """
    #     # def sh_pacmod_type(d_pacmod: TyDic, type_: str) -> str:
    #     package = d_pacmod['package']
    #     module = d_pacmod['module']
    #     return f"/data/{package}/{module}/{type_}"

    # @classmethod
    # def sh_file_path(
    #         cls, d_pacmod: TyDic, type_: str, suffix: str,
    #         pid: Any, ts: Any, **kwargs) -> str:
    #     """ show type specific path
    #     """
    #     filename_ = kwargs.get('filename', type_)
    #     sw_run_pid_ts = kwargs.get('sw_run_pid_ts', True)
    #     if sw_run_pid_ts is None:
    #         sw_run_pid_ts = True
    #
    #   _dir: str = cls.sh_pacmod_type(d_pacmod, type_)
    #   if sw_run_pid_ts:
    #       file_path = os_path.join(
    #           _dir, f"{filename_}_{pid}_{ts}.{suffix}")
    #   else:
    #       file_path = os_path.join(_dir, f"{filename_}.{suffix}")
    #   return file_path

    @staticmethod
    def sh_dir_type(com, type_: str) -> TyPath:
        """Show run_dir
        """
        dir_dat: str = com.dir_dat
        tenant: str = com.tenant
        package: str = com.d_app_pacmod['package']
        module: str = com.d_app_pacmod['module']
        if not tenant:
            return f"{dir_dat}/{tenant}/{package}/{module}/{type_}"
        else:
            return f"{dir_dat}/{package}/{module}/{type_}"

    @classmethod
    def sh_path_pattern(
            cls, com, filename, type_: str, suffix: str) -> TyPath:
        """ show type specific path
        """
        _dir: str = cls.sh_dir_type(com, type_)
        return os_path.join(_dir, f"{filename}*.{suffix}")
