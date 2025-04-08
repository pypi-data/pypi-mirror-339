# coding=utf-8
from ka_uts_com.utils.doeq import DoEq

from typing import Any
TyArr = list[Any]
TyDic = dict[Any, Any]

TnArr = None | TyArr
TnDic = None | TyDic
TnStr = None | str


class AoEqStmt:
    """ Dictionary of Equates
    """
    @staticmethod
    def init_d_eq(a_eqstmt: TyArr) -> TyDic:
        d_eq = {}
        for s_eq in a_eqstmt[1:]:
            a_eq = s_eq.split('=')
            if len(a_eq) == 1:
                d_eq['cmd'] = a_eq[0]
            else:
                d_eq[a_eq[0]] = a_eq[1]
                d_eq[a_eq[0]] = a_eq[1]
        return d_eq

    @classmethod
    def sh_d_eq(cls, a_eqstmt: TyArr, **kwargs) -> TyDic:
        """ show equates dictionary
        """
        d_parms: TnDic = kwargs.get('d_parms')
        _sh_prof = kwargs.get('sh_prof')
        d_eq: TyDic = cls.init_d_eq(a_eqstmt)
        d_eq_new: TyDic = DoEq.verify(d_eq, d_parms)
        DoEq._set_sh_prof(d_eq_new, _sh_prof)
        return d_eq_new
