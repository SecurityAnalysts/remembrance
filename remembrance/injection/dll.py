from abc import ABC, abstractmethod

from remembrance.memory import Memory, MemoryProtection
from remembrance.native import Kernel32


class DLLInjectionMethod(ABC):
    _memory: Memory

    # noinspection PyUnresolvedReferences
    def __init__(self, process: "Process"):
        self._memory = Memory(process)

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class DLLLoadLibraryMethod(DLLInjectionMethod):
    def execute(self, dll_path: str):
        """
        Load the DLL using LoadLibrary and CreateRemoteThread.
        :param dll_path: the path to the DLL
        :return: the dll path memory area and the DLL thread
        """
        path_area = self._memory.allocate_area(len(dll_path), MemoryProtection.PAGE_READWRITE)
        path_area.write(dll_path.encode('ascii'))

        # noinspection PyProtectedMember
        loadlibrary_address = Kernel32.GetProcAddress(Kernel32._handle, b"LoadLibraryA")

        thread = self._memory.process.create_thread(loadlibrary_address, param=path_area.base_address)

        return path_area, thread
