import functools
from ctypes.wintypes import HANDLE
from typing import Callable

from .exception import HandleException
from .native import Kernel32
from .native.exception import WinAPIException


def _ensure_handle_not_closed(function: Callable):
    @functools.wraps(function)
    def wrapper(cls: "Handle", *args, **kwargs):
        if cls.__getattribute__("_Handle__handle") is None:
            raise HandleException("The handle is not open.")

        return function(cls, *args, **kwargs)

    return wrapper


class Handle:
    __handle: HANDLE

    @property
    @_ensure_handle_not_closed
    def native(self) -> HANDLE:
        """ Get the handle as a ctypes.wintypes HANDLE object. """
        return self.__handle

    @property
    @_ensure_handle_not_closed
    def value(self) -> int:
        """ Get the handle value as an integer. """
        return self.__handle.value

    @property
    def open(self) -> bool:
        """ If the handle is open. """
        return self.__handle is not None

    def __init__(self, native_handle: HANDLE):
        self.__handle = native_handle

    @staticmethod
    def invalid() -> "Handle":
        # noinspection PyTypeChecker
        return Handle(None)

    @_ensure_handle_not_closed
    def close(self):
        """ Close the handle. """
        if not Kernel32.CloseHandle(self.__handle):
            raise WinAPIException

        # noinspection PyTypeChecker
        self.__handle = None

    def __str__(self) -> str:
        return f"Handle(value={f'{self.__handle:#x}' if self.__handle else None}, open={self.open})"

    def __repr__(self) -> str:
        return self.__str__()
