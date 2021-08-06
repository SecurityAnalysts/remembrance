import ctypes
from ctypes.wintypes import *

PVOID = ctypes.c_void_p
ULONG64 = ctypes.c_ulonglong

if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ULONG64
else:
    ULONG_PTR = ULONG

NTSTATUS = ULONG
SIZE_T = ULONG
PSIZE_T = ctypes.POINTER(SIZE_T)
FARPROC = LPVOID
