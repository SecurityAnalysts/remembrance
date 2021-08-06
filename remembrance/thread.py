import ctypes
import enum
from _winapi import INVALID_HANDLE_VALUE
from ctypes.wintypes import ULONG
from typing import List

from .exception import ThreadException
from .handle import Handle
from .native import Kernel32, NTDLL, PVOID
from .native.constants import THREAD_PRIORITY_ERROR_RETURN
from .native.enum import SnapshotFlags, ThreadContextFlags, ThreadInfoClass
from .native.exception import NTSTATUS_SUCCESS, NTSTATUSException, WinAPIException
from .native.structure import CONTEXT64, THREADENTRY32


class ThreadAccessRights(enum.IntEnum):
    DELETE = 0x00010000
    READ_CONTROL = 0x00020000
    SYNCHRONIZE = 0x00100000
    WRITE_DAC = 0x00040000
    WRITE_OWNER = 0x00080000

    THREAD_DIRECT_IMPERSONATION = 0x0200
    THREAD_GET_CONTEXT = 0x0008
    THREAD_IMPERSONATE = 0x0100
    THREAD_QUERY_INFORMATION = 0x0040
    THREAD_QUERY_LIMITED_INFORMATION = 0x0800
    THREAD_SET_CONTEXT = 0x0010
    THREAD_SET_INFORMATION = 0x0020
    THREAD_SET_LIMITED_INFORMATION = 0x0400
    THREAD_SET_THREAD_TOKEN = 0x0080
    THREAD_SUSPEND_RESUME = 0x0002
    THREAD_TERMINATE = 0x0001

    THREAD_ALL_ACCESS = (
            THREAD_DIRECT_IMPERSONATION | THREAD_GET_CONTEXT |
            THREAD_IMPERSONATE | THREAD_QUERY_INFORMATION |
            THREAD_QUERY_LIMITED_INFORMATION | THREAD_SET_THREAD_TOKEN |
            THREAD_SET_INFORMATION | THREAD_SET_LIMITED_INFORMATION |
            THREAD_SET_THREAD_TOKEN | THREAD_SUSPEND_RESUME |
            THREAD_TERMINATE | SYNCHRONIZE)


class Thread:
    __tid: int
    __handle: Handle

    @property
    def tid(self) -> int:
        """ The thread ID. """
        return self.__tid

    @property
    def handle(self) -> Handle:
        """ The thread handle. """
        return self.__handle

    @property
    def start_address(self) -> int:
        """ The thread start address. """
        start_address = PVOID()
        data_size = ULONG()

        status = NTDLL.NtQueryInformationThread(self.__handle.native, ThreadInfoClass.ThreadQuerySetWin32StartAddress,
                                                ctypes.pointer(start_address), ctypes.sizeof(PVOID),
                                                ctypes.pointer(data_size))
        if status != NTSTATUS_SUCCESS:
            raise NTSTATUSException(status)

        return start_address.value

    @property
    def priority(self) -> int:
        """ The thread priority. """
        priority = Kernel32.GetThreadPriority(self.__handle.native)
        if priority == THREAD_PRIORITY_ERROR_RETURN:
            raise WinAPIException

        return priority

    @priority.setter
    def priority(self, priority: int):
        if not Kernel32.SetThreadPriority(self.__handle.native, priority):
            raise WinAPIException

    def __init__(self, thread_id: int, handle: Handle = Handle.invalid()):
        self.__tid = thread_id
        self.__handle = handle

    @staticmethod
    def all():
        """ Get all threads running on the machine. """
        entry = THREADENTRY32()
        entry.dwSize = ctypes.sizeof(THREADENTRY32)

        snapshot = Kernel32.CreateToolhelp32Snapshot(SnapshotFlags.TH32CS_SNAPTHREAD, 0)
        if snapshot == INVALID_HANDLE_VALUE:
            raise WinAPIException

        if not Kernel32.Thread32First(snapshot, ctypes.pointer(entry)):
            Kernel32.CloseHandle(snapshot)
            raise WinAPIException

        thread_ids = []
        while Kernel32.Thread32Next(snapshot, ctypes.pointer(entry)):
            thread_ids.append(entry.th32ThreadID)

        Kernel32.CloseHandle(snapshot)

        return [Thread(tid) for tid in thread_ids]

    # noinspection PyUnresolvedReferences
    @staticmethod
    def all_of(process: "Process") -> List["Thread"]:
        """
        Get all threads owned by the provided process.
        :param process: the parent process
        :return: the list of threads
        """
        entry = THREADENTRY32()
        entry.dwSize = ctypes.sizeof(THREADENTRY32)

        snapshot = Kernel32.CreateToolhelp32Snapshot(SnapshotFlags.TH32CS_SNAPTHREAD, 0)
        if snapshot == INVALID_HANDLE_VALUE:
            raise WinAPIException

        if not Kernel32.Thread32First(snapshot, ctypes.pointer(entry)):
            Kernel32.CloseHandle(snapshot)
            raise WinAPIException

        matching_tids = []
        while Kernel32.Thread32Next(snapshot, ctypes.pointer(entry)):
            if process.pid == entry.th32OwnerProcessID:
                matching_tids.append(entry.th32ThreadID)

        Kernel32.CloseHandle(snapshot)

        return [Thread(tid) for tid in matching_tids]

    # noinspection PyUnresolvedReferences
    @staticmethod
    def main_of(process: "Process") -> "Thread":
        """
        Get the main thread of a process.
        NOTE: All it does is pick the first element of Thread.all_of.
        :param process: the parent process
        :return: the main process thread
        """
        return Thread.all_of(process)[0]

    def open(self, access_rights: ThreadAccessRights, inheritable: bool = False):
        """
        Open the thread to get its handle and to be able to manipulate it.
        :param access_rights: the desired access rights
        :param inheritable: if the handle can be inheritable
        """
        if self.__handle.open:
            raise ThreadException("Process is already open.")

        native_handle = Kernel32.OpenThread(access_rights, inheritable, self.__tid)
        if native_handle is None:
            raise WinAPIException

        self.__handle = Handle(native_handle)

    def close(self):
        """ Close the previously opened thread handle. """
        self.__handle.close()

    def suspend(self):
        """ Suspend the thread execution. """
        Kernel32.SuspendThread(self.__handle.native)

    def resume(self):
        """ Resume the process execution. """
        Kernel32.ResumeThread(self.__handle.native)

    def terminate(self, exit_code: int = 0x0):
        """
        Terminate the thread.
        :param exit_code: the thread exit code
        """
        Kernel32.TerminateThread(self.__handle.native, exit_code)

    def wait(self, wait_time: int = -1):
        """
        Wait for the thread execution.
        :param wait_time: the wait time
        :return:
        """
        Kernel32.WaitForSingleObjectEx(self.__handle.native, wait_time, True)

    def hijack(self, new_address: int):
        """
        Hijack the thread and start to execute the code at the new address.
        NOTE: If THREAD_ALL_ACCESS is used, it will throw error, for some reason.
        NOTE: It only works on x64 threads.
        :param new_address: the new code address
        """
        self.suspend()

        context = CONTEXT64()
        context.ContextFlags = ThreadContextFlags.CONTEXT_FULL

        if not Kernel32.GetThreadContext(self.__handle.native, ctypes.pointer(context)):
            self.resume()
            raise WinAPIException

        context.Rip = new_address

        if not Kernel32.SetThreadContext(self.__handle.native, ctypes.pointer(context)):
            self.resume()
            raise WinAPIException

        self.resume()

    def __str__(self) -> str:
        return f"Thread(tid={self.__tid}, handle={self.__handle})"

    def __repr__(self) -> str:
        return self.__str__()
