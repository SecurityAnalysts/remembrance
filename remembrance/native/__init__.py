import ctypes
from ctypes.wintypes import *

from remembrance.native.structure import LPCONTEXT64, LPPROCESSENTRY32A, LPTHREADENTRY32
from remembrance.native.types import FARPROC, NTSTATUS, PSIZE_T, PVOID, SIZE_T

Kernel32 = ctypes.windll.Kernel32

"""
    BOOL CloseHandle(
        HANDLE hObject
    );
"""
Kernel32.CloseHandle.argtypes = [HANDLE]
Kernel32.CloseHandle.restype = BOOL

"""
    _Post_equals_last_error_ DWORD GetLastError();
"""
Kernel32.GetLastError.argtypes = []
Kernel32.GetLastError.restype = DWORD

"""
    HANDLE OpenProcess(
        DWORD dwDesiredAccess,
        BOOL  bInheritHandle,
        DWORD dwProcessId
    );
"""
Kernel32.OpenProcess.argtypes = [DWORD, BOOL, DWORD]
Kernel32.OpenProcess.restype = HANDLE

"""
    HANDLE CreateToolhelp32Snapshot(
        DWORD dwFlags,
        DWORD th32ProcessID
    );
"""
Kernel32.CreateToolhelp32Snapshot.argtypes = [DWORD, DWORD]
Kernel32.CreateToolhelp32Snapshot.restype = HANDLE

"""
    BOOL Process32First(
        HANDLE           hSnapshot,
        LPPROCESSENTRY32 lppe
    );
"""
Kernel32.Process32First.argtypes = [HANDLE, LPPROCESSENTRY32A]
Kernel32.Process32First.restype = BOOL

"""
    BOOL Process32Next(
        HANDLE           hSnapshot,
        LPPROCESSENTRY32 lppe
    );
"""
Kernel32.Process32Next.argtypes = [HANDLE, LPPROCESSENTRY32A]
Kernel32.Process32Next.restype = BOOL

"""
    BOOL QueryFullProcessImageNameA(
        HANDLE hProcess,
        DWORD  dwFlags,
        LPSTR  lpExeName,
        PDWORD lpdwSize
    );
"""
Kernel32.QueryFullProcessImageNameA.argtypes = [HANDLE, DWORD, LPSTR, PDWORD]
Kernel32.QueryFullProcessImageNameA.restype = DWORD

"""
    BOOL Thread32First(
        HANDLE           hSnapshot,
        LPTHREADENTRY32  lpte
    );
"""
Kernel32.Thread32First.argtypes = [HANDLE, LPTHREADENTRY32]
Kernel32.Thread32First.restype = BOOL

"""
    BOOL Thread32Next(
        HANDLE           hSnapshot,
        LPTHREADENTRY32  lpte
    );
"""
Kernel32.Thread32Next.argtypes = [HANDLE, LPTHREADENTRY32]
Kernel32.Thread32Next.restype = BOOL

"""
    HANDLE OpenThread(
        DWORD dwDesiredAccess,
        BOOL  bInheritHandle,
        DWORD dwThreadId
    );
"""
Kernel32.OpenThread.argtypes = [DWORD, BOOL, DWORD]
Kernel32.OpenThread.restype = HANDLE

"""
    DWORD SuspendThread(
        HANDLE hThread
    );
"""
Kernel32.SuspendThread.argtypes = [HANDLE]
Kernel32.SuspendThread.restype = DWORD

"""
    DWORD ResumeThread(
        HANDLE hThread
    );
"""
Kernel32.ResumeThread.argtypes = [HANDLE]
Kernel32.ResumeThread.restype = DWORD

"""
    DWORD TerminateThread(
        HANDLE hThread,
        NTSTATUS ntExitCode
    );
"""
Kernel32.TerminateThread.argtypes = [HANDLE, NTSTATUS]
Kernel32.TerminateThread.restype = DWORD

"""
    BOOL WriteProcessMemory(
        HANDLE  hProcess,
        LPVOID  lpBaseAddress,
        LPCVOID lpBuffer,
        SIZE_T  nSize,
        SIZE_T  *lpNumberOfBytesWritten
    );
"""
Kernel32.WriteProcessMemory.argtypes = [HANDLE, LPVOID, LPCVOID, SIZE_T, PSIZE_T]
Kernel32.WriteProcessMemory.restype = BOOL

"""
    BOOL ReadProcessMemory(
        HANDLE  hProcess,
        LPCVOID lpBaseAddress,
        LPVOID  lpBuffer,
        SIZE_T  nSize,
        SIZE_T  *lpNumberOfBytesRead
    );
"""
Kernel32.ReadProcessMemory.argtypes = [HANDLE, LPCVOID, LPVOID, SIZE_T, PSIZE_T]
Kernel32.ReadProcessMemory.restype = BOOL

"""
    LPVOID VirtualAllocEx(
        HANDLE hProcess,
        LPVOID lpAddress,
        SIZE_T dwSize,
        DWORD  flAllocationType,
        DWORD  flProtect
    );
"""
Kernel32.VirtualAllocEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD, DWORD]
Kernel32.VirtualAllocEx.restype = LPVOID

"""
    BOOL VirtualFreeEx(
        HANDLE hProcess,
        LPVOID lpAddress,
        SIZE_T dwSize,
        DWORD  dwFreeType
    );
"""
Kernel32.VirtualFreeEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD]
Kernel32.VirtualFreeEx.restype = BOOL

"""
    int GetThreadPriority(
        HANDLE hThread
    );
"""
Kernel32.GetThreadPriority.argtypes = [HANDLE]
Kernel32.GetThreadPriority.restype = INT

"""
    BOOL SetThreadPriority(
        HANDLE hThread,
        int    nPriority
    );
"""
Kernel32.SetThreadPriority.argtypes = [HANDLE, INT]
Kernel32.SetThreadPriority.restype = BOOL

"""
    HANDLE CreateRemoteThread(
        HANDLE                 hProcess,
        LPSECURITY_ATTRIBUTES  lpThreadAttributes,
        SIZE_T                 dwStackSize,
        LPTHREAD_START_ROUTINE lpStartAddress,
        LPVOID                 lpParameter,
        DWORD                  dwCreationFlags,
        LPDWORD                lpThreadId
    );
"""
Kernel32.CreateRemoteThread.argtypes = [HANDLE, LPVOID, SIZE_T, LPCVOID, LPVOID, DWORD, LPDWORD]
Kernel32.CreateRemoteThread.restype = HANDLE

"""
    FARPROC GetProcAddress(
        HMODULE hModule,
        LPCSTR  lpProcName
    );
"""
Kernel32.GetProcAddress.argtypes = [HMODULE, LPCSTR]
Kernel32.GetProcAddress.restype = FARPROC

"""
    BOOL GetThreadContext(
        HANDLE    hThread,
        LPCONTEXT lpContext
    );
"""
Kernel32.GetThreadContext.argtypes = [HANDLE, LPCONTEXT64]
Kernel32.GetThreadContext.restype = BOOL

"""
    BOOL SetThreadContext(
        HANDLE        hThread,
        const CONTEXT *lpContext
    );
"""
Kernel32.SetThreadContext.argtypes = [HANDLE, LPCONTEXT64]
Kernel32.SetThreadContext.restype = BOOL

#######################################################################################
# NTDLL Stuff

NTDLL = ctypes.windll.NTDLL

"""
    NTSTATUS NtSuspendProcess(
        HANDLE hProcess
    );
"""
NTDLL.NtSuspendProcess.argtypes = [HANDLE]
NTDLL.NtSuspendProcess.restype = NTSTATUS

"""
    NTSTATUS NtResumeProcess(
        HANDLE hProcess
    );
"""
NTDLL.NtResumeProcess.argtypes = [HANDLE]
NTDLL.NtResumeProcess.restype = NTSTATUS

"""
    NTSTATUS NtTerminateProcess(
        HANDLE hProcess,
        NTSTATUS ntExitCode
    );
"""
NTDLL.NtTerminateProcess.argtypes = [HANDLE, NTSTATUS]
NTDLL.NtTerminateProcess.restype = NTSTATUS

"""
    __kernel_entry NTSTATUS NtQueryInformationThread(
        HANDLE          ThreadHandle,
        THREADINFOCLASS ThreadInformationClass,
        PVOID           ThreadInformation,
        ULONG           ThreadInformationLength,
        PULONG          ReturnLength
    );
"""
NTDLL.NtQueryInformationThread.argtypes = [HANDLE, DWORD, PVOID, ULONG, PULONG]
