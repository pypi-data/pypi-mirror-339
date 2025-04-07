# coding=utf-8
import yaml

from typing import Any
TyAny = Any
TyArr = list[Any]
TyDic = dict[Any, Any]

TnAny = None | Any


class Yaml_:
    """ Manage Object to Yaml file affilitation
    """
    @staticmethod
    def read(path: str, log) -> TnAny:
        try:
            with open(path) as fd:
                # The Loader parameter handles the conversion from YAML
                # scalar values to Python object format
                obj = yaml.load(fd, Loader=yaml.SafeLoader)
                return obj
        except FileNotFoundError:
            log.error(f"No such file or directory: {path}")
        except IOError:
            # if Com.Log is not None:
            #     fnc_error = Com.Log.error
            #     fnc_error(exc, exc_info=True)
            raise
        return None
