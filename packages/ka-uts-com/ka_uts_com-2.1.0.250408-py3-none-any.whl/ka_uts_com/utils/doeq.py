# coding=utf-8
from collections.abc import Callable
from typing import Any

# from ka_uts_com.utils.pacmod import PacMod
from ka_uts_com.utils.str import Str
from ka_uts_com.utils.date import Date


TyArr = list[Any]
TyCall = Callable[..., Any]
TyDic = dict[Any, Any]
TyStr = str

TnArr = None | TyArr
TnDic = None | TyDic
TnStr = None | TyStr


class DoEq:
    """ Manage Commandline Arguments
    """
    @classmethod
    def sh_value(cls, key: str, value: Any, d_valid_parms: TnDic) -> Any:

        # print(f"key = {key}, type(key) = {type(key)}")
        # print(f"value = {value}, type(value) = {type(value)}")
        if not d_valid_parms:
            return value
        _type: TnStr = d_valid_parms.get(key)
        # print(f"_type = {_type}")
        if not _type:
            return value
        if isinstance(_type, str):
            match _type:
                case 'int':
                    value = int(value)
                case 'bool':
                    value = Str.sh_boolean(value)
                case 'dict':
                    value = Str.sh_dic(value)
                case 'list':
                    value = Str.sh_arr(value)
                case '%Y-%m-%d':
                    value = Date.sh(value, _type)
                case '_':
                    match _type[0]:
                        case '[', '{':
                            _obj = Str.sh_dic(_type)
                            if value not in _obj:
                                msg = (f"parameter={key} value={value} is invalid; "
                                       f"valid values are={_obj}")
                                raise Exception(msg)

        # print(f"value = {value}, type(value) = {type(value)}")
        return value

    # @staticmethod
    # def _set_d_pacmod(d_eq: TyDic, root_cls) -> None:
    #   """ set current pacmod dictionary
    #   """
    #   tenant = d_eq.get('tenant')
    #   d_eq['d_pacmod'] = PacMod.sh_d_pacmod(root_cls, tenant)

    @staticmethod
    def _set_sh_prof(d_eq: TyDic, sh_prof: TyCall | Any) -> None:
        """ set current pacmod dictionary
        """
        if callable(sh_prof):
            d_eq['sh_prof'] = sh_prof()
        else:
            d_eq['sh_prof'] = sh_prof

    @classmethod
    def verify(cls, d_eq: TyDic, d_parms: TnDic) -> TyDic:
        if d_parms is None:
            return d_eq
        if 'cmd' in d_eq:
            _d_valid_parms = d_parms
            _cmd = d_eq['cmd']
            _valid_commands = list(d_parms.keys())
            if _cmd not in _valid_commands:
                msg = (f"Wrong command: {_cmd}; "
                       f"valid commands are: {_valid_commands}")
                raise Exception(msg)
            _d_valid_parms = d_parms[_cmd]
        else:
            _d_valid_parms = d_parms
        if _d_valid_parms is None:
            return d_eq

        d_eq_new = {}
        for key, value in d_eq.items():
            if key not in _d_valid_parms:
                msg = (f"Wrong parameter: {key}; "
                       f"valid parameters are: {_d_valid_parms}")
                raise Exception(msg)
            d_eq_new[key] = cls.sh_value(key, value, _d_valid_parms)
        return d_eq_new
