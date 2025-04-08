# coding=utf-8
from typing import Any

import os
import importlib.resources as resources

TyArr = list[Any]
TyDic = dict[Any, Any]
TyPackage = str
TyPackages = list[str]
TyPath = str


class Pac:

    @staticmethod
    def sh_path_by_package(package: TyPackage, path: TyPath) -> Any:
        """ show directory
        """
        _path = str(resources.files(package).joinpath(path))
        # if _path.is_file():
        if _path is not None and _path != '':
            if os.path.exists(_path):
                return _path
        return ''

    @classmethod
    def sh_path_by_packages(cls, packages: TyPackages, path: TyPath) -> Any:
        """ show directory
        """
        for _package in packages:
            _path = cls.sh_path_by_package(_package, path)
            if _path:
                return _path
        return ''
