import ctypes
from ctypes.wintypes import *

from remembrance.native.types import DWORD64, ULONG_PTR


class PROCESSENTRY32A(ctypes.Structure):
    _fields_ = [('dwSize', DWORD),
                ('cntUsage', DWORD),
                ('th32ProcessID', DWORD),
                ('th32DefaultHeapID', ULONG_PTR),
                ('th32ModuleID', DWORD),
                ('cntThreads', DWORD),
                ('th32ParentProcessID', DWORD),
                ('pcPriClassBase', LONG),
                ('dwFlags', DWORD),
                ('szExeFile', CHAR * MAX_PATH)]


LPPROCESSENTRY32A = ctypes.POINTER(PROCESSENTRY32A)


class THREADENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', DWORD),
                ('cntUsage', DWORD),
                ('th32ThreadID', DWORD),
                ('th32OwnerProcessID', DWORD),
                ('tpBasePri', LONG),
                ('tpDeltaPri', LONG),
                ('dwFlags', DWORD)]


LPTHREADENTRY32 = ctypes.POINTER(THREADENTRY32)


class M128A(ctypes.Structure):
    _fields_ = [("Low", DWORD64),
                ("High", DWORD64)]


class XMM_SAVE_AREA32(ctypes.Structure):
    _fields_ = [('ControlWord', WORD),
                ('StatusWord', WORD),
                ('TagWord', BYTE),
                ('Reserved1', BYTE),
                ('ErrorOpcode', WORD),
                ('ErrorOffset', DWORD),
                ('ErrorSelector', WORD),
                ('Reserved2', WORD),
                ('DataOffset', DWORD),
                ('DataSelector', WORD),
                ('Reserved3', WORD),
                ('MxCsr', DWORD),
                ('MxCsr_Mask', DWORD),
                ('FloatRegisters', M128A * 8),
                ('XmmRegisters', M128A * 16),
                ('Reserved4', BYTE * 96)]


class _CONTEXT64_DUMMYSTRUCTNAME(ctypes.Structure):
    _fields_ = [("Header", M128A * 2),
                ("Legacy", M128A * 8),
                ("Xmm0", M128A),
                ("Xmm1", M128A),
                ("Xmm2", M128A),
                ("Xmm3", M128A),
                ("Xmm4", M128A),
                ("Xmm5", M128A),
                ("Xmm6", M128A),
                ("Xmm7", M128A),
                ("Xmm8", M128A),
                ("Xmm9", M128A),
                ("Xmm10", M128A),
                ("Xmm11", M128A),
                ("Xmm12", M128A),
                ("Xmm13", M128A),
                ("Xmm14", M128A),
                ("Xmm15", M128A)]


class _CONTEXT64_DUMMYUNIONNAME(ctypes.Union):
    _fields_ = [("FltSave", XMM_SAVE_AREA32),
                ("DummyStruct", _CONTEXT64_DUMMYSTRUCTNAME)]


class CONTEXT64(ctypes.Structure):
    _fields_ = [("P1Home", DWORD64),
                ("P2Home", DWORD64),
                ("P3Home", DWORD64),
                ("P4Home", DWORD64),
                ("P5Home", DWORD64),
                ("P6Home", DWORD64),
                ("ContextFlags", DWORD),
                ("MxCsr", DWORD),
                ("SegCs", WORD),
                ("SegDs", WORD),
                ("SegEs", WORD),
                ("SegFs", WORD),
                ("SegGs", WORD),
                ("SegSs", WORD),
                ("EFlags", DWORD),
                ("Dr0", DWORD64),
                ("Dr1", DWORD64),
                ("Dr2", DWORD64),
                ("Dr3", DWORD64),
                ("Dr6", DWORD64),
                ("Dr7", DWORD64),
                ("Rax", DWORD64),
                ("Rcx", DWORD64),
                ("Rdx", DWORD64),
                ("Rbx", DWORD64),
                ("Rsp", DWORD64),
                ("Rbp", DWORD64),
                ("Rsi", DWORD64),
                ("Rdi", DWORD64),
                ("R8", DWORD64),
                ("R9", DWORD64),
                ("R10", DWORD64),
                ("R11", DWORD64),
                ("R12", DWORD64),
                ("R13", DWORD64),
                ("R14", DWORD64),
                ("R15", DWORD64),
                ("Rip", DWORD64),
                ("DebugControl", DWORD64),
                ("LastBranchToRip", DWORD64),
                ("LastBranchFromRip", DWORD64),
                ("LastExceptionToRip", DWORD64),
                ("LastExceptionFromRip", DWORD64),
                ("DUMMYUNIONNAME", _CONTEXT64_DUMMYUNIONNAME),
                ("VectorRegister", M128A * 26),
                ("VectorControl", DWORD64)]


LPCONTEXT64 = ctypes.POINTER(CONTEXT64)
