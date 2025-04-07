from ka_uts_com.com import Com
from typing import Any
TyDic = dict[Any, Any]


class Log:
    """Logging Class
    """
    class Eq:

        @classmethod
        def error(cls, key: Any, value: Any) -> None:
            Log.error(f"{key} = {value}", stacklevel=3)

        @classmethod
        def warning(cls, key: Any, value: Any) -> None:
            Log.warning(f"{key} = {value}", stacklevel=3)

        @classmethod
        def info(cls, key: Any, value: Any) -> None:
            Log.info(f"{key} = {value}", stacklevel=3)

        @classmethod
        def log(cls, key: Any, value: Any) -> None:
            Log.log(f"{key} = {value}", stacklevel=3)

        @classmethod
        def debug(cls, key: Any, value: Any) -> None:
            Log.debug(f"{key} = {value}", stacklevel=3)

    class Dic:

        @classmethod
        def debug(cls, dic: TyDic) -> None:
            for key, value in dic.items():
                Log.debug(f"{key} = {value}", stacklevel=3)

        @classmethod
        def error(cls, dic: TyDic) -> None:
            for key, value in dic.items():
                Log.error(f"{key} = {value}", stacklevel=3)

        @classmethod
        def info(cls, dic: TyDic) -> None:
            for key, value in dic.items():
                Log.info(f"{key} = {value}", stacklevel=3)

        @classmethod
        def warning(cls, dic: TyDic) -> None:
            for key, value in dic.items():
                Log.warning(f"{key} = {value}", stacklevel=3)

    @staticmethod
    def error(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.error(*args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.warning(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.info(*args, **kwargs)

    @staticmethod
    def log(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.log(*args, **kwargs)

    @staticmethod
    def debug(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.debug(*args, **kwargs)
