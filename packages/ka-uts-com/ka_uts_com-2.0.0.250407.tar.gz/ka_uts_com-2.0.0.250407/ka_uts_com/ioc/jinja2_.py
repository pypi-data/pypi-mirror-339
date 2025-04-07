# coding=utf-8
# from collections.abc import Callable
from typing import Any

import os
import yaml
import jinja2
# import logging
# import logging.config
from logging import Logger

TyAny = Any
TyDic = dict[Any, Any]
TyLogger = Logger

TnDic = None | TyDic


class Jinja2_:

    """ Manage Object to Json file affilitation
    """
    @staticmethod
    def read_template(path: str) -> Any:
        directory, file = os.path.split(path)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(directory))
        return env.get_template(file)

    @classmethod
    def read(cls, path: str, log: TyLogger, **kwargs) -> Any:
        try:
            # read jinja template from file
            template = cls.read_template(path)
            # render template as yaml string
            template_rendered = template.render(kwargs)
            # load yaml string into object
            obj: Any = yaml.safe_load(template_rendered)
            return obj
        except IOError as exc:
            log.error(exc, exc_info=True)
            # log.error(f"No such file or directory: {path}")
            raise
