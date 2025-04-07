from collections.abc import Sequence
from typing import Any, TypeAlias, Literal

import openpyxl as op
import pandas as pd
import polars as pl

from ka_uts_obj.path import Path
from ka_uts_xls.ioipath import IoiPathWbPd, IoiPathWbOp

TyWbOp: TypeAlias = op.workbook.workbook.Workbook
TyWsOp: TypeAlias = op.worksheet.worksheet.Worksheet
TyPdDf: TypeAlias = pd.DataFrame
TyPlDf: TypeAlias = pl.DataFrame

TyArr = list[Any]
TyDic = dict[Any, Any]
TyAoA = list[TyArr]
TyAoD = list[TyDic]
TyDoAoD = dict[Any, TyAoD]
TyDoPdDf = dict[str, TyPdDf] | dict[Any, TyPdDf]
TyDoPlDf = dict[str, TyPlDf] | dict[Any, TyPlDf]
TyDoWsOp = dict[Any, TyWsOp]
TyAoD_DoAoD = TyAoD | TyDoAoD
TyPdDf_DoPdDf = TyPdDf | dict[str, TyPdDf] | dict[Any, TyPdDf]
TyPlDf_DoPlDf = TyPlDf | TyDoPlDf
TyPath = str
TyPathnm = str

TyPlSheetsId = int | Sequence[int] | Literal[0]
TyPlSheetsNm = str | list[str] | tuple[str]
TyPlSheets = TyPlSheetsId | TyPlSheetsNm

TySheet = int | str
TySheets = int | str | list[int | str]
TySheetname = str
TySheetnames = list[TySheetname]

TnAoD = None | TyAoD
TnAoD_DoAoD = None | TyAoD_DoAoD
TnDoAoD = None | TyDoAoD
TnPdDf = None | TyPdDf
TnPdDf_DoPdDf = None | TyPdDf_DoPdDf
TnDoPdDf = None | TyDoPdDf
TnPlDf = None | TyPlDf
TnPlDf_DoPlDf = None | TyPlDf_DoPlDf
TnPlSheetsId = None | TyPlSheetsId
TnPlSheetsNm = None | TyPlSheetsNm
TnPlSheets = None | TyPlSheets
TnSheet = None | TySheet
TnSheets = None | TySheets
TnSheetname = None | TySheetname
TnSheetnames = None | TySheetnames
TnWbOp = None | TyWbOp
TnWsOp = None | TyWsOp
TnPath = None | TyPath


class IoiPathnmWbPd:

    @staticmethod
    def read_wb_to_aod(
            pathnm: TyPath, sheet: TnSheet, kwargs: TyDic, **kwargs_wb) -> TnAoD:
        aod: TnAoD = IoiPathWbPd.read_wb_to_aod(
                Path.sh_path_using_pathnm(pathnm, **kwargs), sheet, **kwargs_wb)
        return aod

    @staticmethod
    def read_wb_to_doaod(
            pathnm: TyPath, sheet: TnSheet, kwargs: TyDic, **kwargs_wb) -> TnDoAoD:
        doaod: TnDoAoD = IoiPathWbPd.read_wb_to_doaod(
                Path.sh_path_using_pathnm(pathnm, **kwargs), **kwargs_wb)
        return doaod

    @staticmethod
    def read_wb_to_aod_or_doaod(
            pathnm: TyPath, sheet: TnSheet, kwargs: TyDic, **kwargs_wb) -> TnAoD_DoAoD:
        obj: TnAoD_DoAoD = IoiPathWbPd.read_wb_to_aod_or_doaod(
                Path.sh_path_using_pathnm(pathnm, **kwargs), sheet, **kwargs_wb)
        return obj

    @staticmethod
    def read_wb_to_df(
            pathnm: TyPath, sheet: TnSheet, kwargs: TyDic, **kwargs_wb) -> TnPdDf:
        return IoiPathWbPd.read_wb_to_df(
                Path.sh_path_using_pathnm(pathnm, **kwargs), sheet, **kwargs_wb)

    @staticmethod
    def read_wb_to_df_or_dodf(
            pathnm: TyPath, sheet: TnSheet, kwargs: TyDic, **kwargs_wb
    ) -> TnPdDf_DoPdDf:
        return IoiPathWbPd.read_wb_to_df_or_dodf(
                Path.sh_path_using_pathnm(pathnm, **kwargs), sheet, **kwargs_wb)

    @staticmethod
    def read_wb_to_dodf(
            pathnm: TyPath, sheet: TnSheet, kwargs: TyDic, **kwargs_wb) -> TnDoPdDf:
        return IoiPathWbPd.read_wb_to_dodf(
                Path.sh_path_using_pathnm(pathnm, **kwargs), sheet, **kwargs_wb)


class IoiPathnmWbOp:

    @staticmethod
    def load(pathnm: str, kwargs: TyDic, **kwargs_wb) -> TyWbOp:
        return IoiPathWbOp.load(
                Path.sh_path_using_pathnm(pathnm, **kwargs), **kwargs_wb)
