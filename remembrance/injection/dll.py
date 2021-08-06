from abc import ABC, abstractmethod
from typing import Tuple

from ..memory import Memory, MemoryProtection
from ..native import Kernel32
from ..thread import Thread


# noinspection PyUnresolvedReferences
class DLLInjectionMethod(ABC):
    _process: "Process"
    _memory: Memory

    def __init__(self, process: "Process"):
        self._process = process
        self._memory = Memory(process)

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class DLLLoadLibraryMethod(DLLInjectionMethod):
    # noinspection PyUnresolvedReferences
    def execute(self, dll_path: bytes) -> Tuple["MemoryArea", Thread]:
        """
        Inject the DLL and execute it using LoadLibrary.
        :param dll_path: the dll path
        :return: the dll path memory area and the dll thread
        """
        area = self._memory.allocate_area(len(dll_path), MemoryProtection.PAGE_READWRITE)
        area.write(dll_path.encode('ascii'))

        # noinspection PyProtectedMember
        loadlibrary_address = Kernel32.GetProcAddress(Kernel32._handle, b"LoadLibraryA")

        thread = self._process.create_thread(loadlibrary_address, param=area.base_address)

        return area, thread
