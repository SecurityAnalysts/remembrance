import ctypes
from ctypes.wintypes import *

PVOID = LPVOID
ULONG64 = ctypes.c_ulonglong
DWORD64 = ULONG64

if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ULONG64
else:
    ULONG_PTR = ULONG

NTSTATUS = ULONG
SIZE_T = ctypes.c_size_t
PSIZE_T = ctypes.POINTER(SIZE_T)
FARPROC = LPVOID
