import openpyxl as op
import pyexcelerate as pe

# from ka_uts_com.log import Log

from typing import Any, TypeAlias
TyWbOp: TypeAlias = op.workbook.workbook.Workbook
TyWbPe: TypeAlias = pe.Workbook

TyPath = str
TnWbOp = None | TyWbOp


class IocWbOp:

    @staticmethod
    def get(**kwargs: Any) -> TyWbOp:
        wb: TyWbOp = op.Workbook(**kwargs)
        return wb


class IocWbPe:

    @staticmethod
    def get(**kwargs: Any) -> TyWbPe:
        wb: TyWbPe = pe.Workbook(**kwargs)
        return wb
