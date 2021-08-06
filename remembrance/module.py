import ctypes
from _winapi import INVALID_HANDLE_VALUE
from typing import List

from remembrance.exception import ModuleNotFoundException
from remembrance.native import Kernel32
from remembrance.native.enum import SnapshotFlags
from remembrance.native.exception import WinAPIException
from remembrance.native.structure import MODULEENTRY32A
from remembrance.process import Process


class Module:
    __parent: Process
    __base_address: int
    __size: int
    __name: str

    @property
    def base_address(self):
        """ The module image base address. """
        return self.__base_address

    @property
    def size(self) -> int:
        """ The module image size. """
        return self.__size

    @property
    def name(self) -> str:
        """ The module name. """
        return self.__name

    def __init__(self, parent: Process, base_address: int, size: int, module_name: str):
        self.__parent = parent
        self.__base_address = base_address
        self.__size = size
        self.__name = module_name

    @staticmethod
    def from_native_structure(parent: Process, entry: MODULEENTRY32A):
        """ Create a Module object from its MODULEENTRY32A structure. """
        return Module(parent, int.from_bytes(entry.modBaseAddr, byteorder='little'),
                      entry.modBaseSize, entry.szModule.decode('utf-8'))

    @staticmethod
    def all_of(process: Process) -> List["Module"]:
        """
        Get all modules owned by the provided process.
        :param process: the parent process
        :return: the list of modules
        """
        entry = MODULEENTRY32A()
        entry.dwSize = ctypes.sizeof(MODULEENTRY32A)

        snapshot = Kernel32.CreateToolhelp32Snapshot(
                SnapshotFlags.TH32CS_SNAPMODULE | SnapshotFlags.TH32CS_SNAPMODULE32, process.pid)
        if snapshot == INVALID_HANDLE_VALUE:
            raise WinAPIException

        if not Kernel32.Module32First(snapshot, ctypes.pointer(entry)):
            Kernel32.CloseHandle(snapshot)
            raise WinAPIException

        modules = []
        while Kernel32.Module32Next(snapshot, ctypes.pointer(entry)):
            modules.append(Module.from_native_structure(process, entry))

        Kernel32.CloseHandle(snapshot)

        return modules

    @staticmethod
    def with_name(process: Process, name: str, case_sensitive: bool = False) -> "Module":
        """
        Get a module by its name.
        :param process: the parent process
        :param name: the module name
        :param case_sensitive: if the name is case sensitive
        :return: the module
        """
        modules = Module.all_of(process)
        module_names = [module.name for module in modules]

        if not case_sensitive:
            name = name.casefold()
            module_names = [name.casefold() for name in module_names]

        if name not in module_names:
            raise ModuleNotFoundException

        return modules[module_names.index(name)]

    def eject(self):
        """ Eject the module from the proces. """
        # noinspection PyProtectedMember
        freelibrary_address = Kernel32.GetProcAddress(Kernel32._handle, b'FreeLibrary')
        self.__parent.create_thread(freelibrary_address, param=self.__base_address)

    def __str__(self) -> str:
        return f"Module(base_address={self.__base_address:#x}, size={self.__size}, name=\"{self.__name}\")"

    def __repr__(self) -> str:
        return self.__str__()
