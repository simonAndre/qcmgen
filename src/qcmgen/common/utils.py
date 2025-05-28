import importlib.util
import sys
import os
from pathlib import Path
from logging import Logger
from uuid import uuid4
from typing import Optional
from .logging_helpers import get_logger

def import_from_source_file(module_name, file_path):
    """Import a source file as a module
     
    Arguments:
        @module_name: the qualified name of the module
        @file_path: the path to the file containing the module's code
         
    If a module with that name already exists in sys.modules,
    nothing is done and the existing module is returned.
     
    This function does not attempt to import the parent module
    nor to insert it in sys.modules.
    """
    try:
        return sys.modules[module_name]
    except KeyError:
        pass
    # from a recipe in importlib.machinery's documentation
    if Path(file_path).is_dir():
        file_path = file_path / '__init__.py'
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(
            'Cannot get module spec from file location', file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class UserError(Exception):
    def __init__(
        self,
        message: str,
        logger: Optional[Logger] = None,
        base_exception: Optional[Exception] = None,
        display_trace: bool = False,
        *args: object,
    ) -> None:
        super().__init__(message, *args)

        self.provide_stack_trace = (base_exception or display_trace) and bool(
            int(os.getenv("OPTION_TRACE_USERERROR", 0))
        )  # 0 or 1
        self.base_exception = base_exception
        if base_exception:
            self.corrid = uuid4()
            self.message = f"correlation_id={self.corrid} -- {message} -- {base_exception}"
        else:
            self.message = message
        if logger:
            self._lgger = logger
        else:
            self._lgger = get_logger("root")

    @property
    def http_code(self) -> int:
        return 400

    def log_and_exit(self):
        if self.provide_stack_trace:
            excinfo = self
        else:
            excinfo = None

        if self.base_exception:
            get_logger("internal").exception(f"correlation_id={self.corrid}", exc_info=self.base_exception)
        self._lgger.exception(msg=self.message, exc_info=excinfo)
        sys.exit(self.message)


class BadArgsError(UserError):
    @property
    def http_code(self) -> int:
        return 400


def print_error(errmsg):
    print("---------------------")
    print(f"qcmgen ERROR: {errmsg}")
    print("---------------------")
    exit(1)