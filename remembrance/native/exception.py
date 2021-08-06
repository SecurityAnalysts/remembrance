import ctypes
from collections import defaultdict

from . import Kernel32
from .ntstatus import NTSTATUS_CODES

DEFAULT_NTSTATUS_CHOICE = 0
NTSTATUS_SUCCESS = 0


class NativeException(Exception):
    ...


class WinAPIException(NativeException, OSError):
    def __init__(self, code: int = None, message: str = None):
        if code is None:
            code = Kernel32.GetLastError()

        if message is None:
            message = ctypes.FormatError(code).strip()  # Yoinked from ctypes WinError

        super().__init__(None, message, None, code)  # Yoinked from ctypes as well


class NTSTATUSException(NativeException):
    STATUS_CODES = defaultdict(list)

    def __init__(self, code: int, message: str = None):
        code = ctypes.c_ulong(code).value

        if message is None:
            message = self.STATUS_CODES[code][DEFAULT_NTSTATUS_CHOICE]

        super().__init__(f"[NTSTATUS {code:#x}] {message}.")

    @classmethod
    def register(cls, code: int, _name: str, description: str):
        cls.STATUS_CODES[code].append(description)


# Register all NTSTATUS codes (I made it this way so that the IDE formatter isn't overwhelmed)
for data in NTSTATUS_CODES:
    NTSTATUSException.register(*data)
