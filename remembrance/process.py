import ctypes
import enum
from _winapi import INVALID_HANDLE_VALUE
from ctypes.wintypes import DWORD, MAX_PATH
from typing import List, Type

from .exception import ProcessException, ProcessNotFoundException
from .handle import Handle
from .injection.dll import DLLInjectionMethod
from .injection.shellcode import ShellcodeInjectionMethod
from .native import Kernel32, NTDLL
from .native.enum import SnapshotFlags
from .native.exception import NTSTATUS_SUCCESS, NTSTATUSException, WinAPIException
from .native.structure import PROCESSENTRY32A
from .thread import Thread


class ProcessAccessRights(enum.IntEnum):
    DELETE = 0x00010000
    READ_CONTROL = 0x00020000
    SYNCHRONIZE = 0x00100000
    WRITE_DAC = 0x00040000
    WRITE_OWNER = 0x00080000

    PROCESS_CREATE_PROCESS = 0x0080
    PROCESS_CREATE_THREAD = 0x0002
    PROCESS_DUP_HANDLE = 0x0040
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    PROCESS_SET_INFORMATION = 0x0200
    PROCESS_SET_QUOTA = 0x0100
    PROCESS_SUSPEND_RESUME = 0x0800
    PROCESS_TERMINATE = 0x0001
    PROCESS_VM_OPERATION = 0x0008
    PROCESS_VM_READ = 0x0010
    PROCESS_VM_WRITE = 0x0020

    PROCESS_ALL_ACCESS = (
            PROCESS_CREATE_PROCESS | PROCESS_CREATE_THREAD |
            PROCESS_DUP_HANDLE | PROCESS_QUERY_INFORMATION |
            PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_SET_INFORMATION |
            PROCESS_SET_QUOTA | PROCESS_SUSPEND_RESUME |
            PROCESS_TERMINATE | PROCESS_VM_OPERATION |
            PROCESS_VM_READ | PROCESS_VM_WRITE |
            SYNCHRONIZE)


class Process:
    __pid: int
    __handle: Handle = Handle.invalid()

    @property
    def pid(self) -> int:
        """ Get the process ID. """
        return self.__pid

    @property
    def handle(self) -> Handle:
        """ Get the Handle object associated with this process. """
        return self.__handle

    @property
    def filename(self) -> str:
        """ Get the process executable file path. """
        path = ctypes.create_string_buffer(MAX_PATH)
        size = DWORD(MAX_PATH)
        if not Kernel32.QueryFullProcessImageNameA(self.__handle.native, 0, path, ctypes.pointer(size)):
            raise WinAPIException

        return path.raw[:size.value].decode('utf-8')

    def __init__(self, process_id: int):
        self.__pid = process_id

    @staticmethod
    def by_name(name: str, case_sensitive: bool = False, allow_multiple: bool = False) -> "Process" or List["Process"]:
        """
        Get a process (or more than one) by its (or their) name.
        :param name: the name to match
        :param case_sensitive: if the name is case-sensitive
        :param allow_multiple: if multiple processes can be returned
        :return: the list of processes if allow_multiple is true, otherwise the matched process
        """
        if not case_sensitive:
            name = name.casefold()

        entry = PROCESSENTRY32A()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32A)

        snapshot = Kernel32.CreateToolhelp32Snapshot(SnapshotFlags.TH32CS_SNAPPROCESS, 0)
        if snapshot == INVALID_HANDLE_VALUE:
            raise WinAPIException

        if not Kernel32.Process32First(snapshot, ctypes.pointer(entry)):
            Kernel32.CloseHandle(snapshot)
            raise WinAPIException

        matching_pids = []
        while Kernel32.Process32Next(snapshot, ctypes.pointer(entry)):
            process_name = entry.szExeFile.decode('utf-8')
            process_name = process_name if case_sensitive else process_name.casefold()

            if name == process_name:
                matching_pids.append(entry.th32ProcessID)

        Kernel32.CloseHandle(snapshot)

        if not matching_pids:
            raise ProcessNotFoundException

        if allow_multiple:
            return [Process(pid) for pid in matching_pids]

        return Process(matching_pids[0])

    def open(self, access_rights: ProcessAccessRights, inheritable: bool = False):
        """
        Open the process to get its handle and to be able to manipulate it.
        :param access_rights: the desired access rights
        :param inheritable: if the handle can be inheritable
        """
        if self.__handle.open:
            raise ProcessException("Process is already open.")

        native_handle = Kernel32.OpenProcess(access_rights, inheritable, self.__pid)
        if native_handle is None:
            raise WinAPIException

        self.__handle = Handle(native_handle)

    def close(self):
        """ Close the previously opened process handle. """
        self.__handle.close()

    def suspend(self):
        """ Suspend the process execution. """
        status = NTDLL.NtSuspendProcess(self.__handle.native)
        if status != NTSTATUS_SUCCESS:
            raise NTSTATUSException(status)

    def resume(self):
        """ Resume the process execution. """
        status = NTDLL.NtResumeProcess(self.__handle.native)
        if status != NTSTATUS_SUCCESS:
            raise NTSTATUSException(status)

    def terminate(self, exit_code: int = 0x0):
        """
        Terminate the process.
        :param exit_code: the process exit code
        """
        status = NTDLL.NtTerminateProcess(self.__handle.native, exit_code)
        if status != NTSTATUS_SUCCESS:
            raise NTSTATUSException(status)

    def create_thread(self, start_address: int, param: int = None, stack_size: int = 0,
                      creation_flags: int = 0) -> Thread:
        """
        Create a thread runniong at the provided start address.
        :param start_address: the address to the code to run
        :param param: the parameter to the thread
        :param stack_size: the thread stack size
        :param creation_flags: the thread creation flags
        :return: the created thread object
        """
        thread_id = DWORD()
        thread_handle = Kernel32.CreateRemoteThread(self.__handle.native, None, stack_size, start_address, param,
                                                    creation_flags, ctypes.pointer(thread_id))
        if thread_handle is None:
            raise WinAPIException

        return Thread(thread_id.value, thread_handle)

    def inject_dll(self, method: Type[DLLInjectionMethod], *args, **kwargs):
        """
        Inject a DLL into the process.
        NOTE: For more parameters, check out the chosen method documentation.
        :param method: the method to use
        """
        return method(self).execute(*args, **kwargs)

    def inject_shellcode(self, method: Type[ShellcodeInjectionMethod], *args, **kwags):
        """
        Inject a shellcode into the process.
        NOTE: For more parameters, check out the chosen method documentation.
        :param method: the method to use
        """
        return method(self).execute(*args, **kwags)

    def __str__(self) -> str:
        return f"Process(pid={self.__pid}, handle={self.__handle})"

    def __repr__(self) -> str:
        return self.__str__()
