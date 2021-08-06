from abc import ABC, abstractmethod
from typing import Tuple

from ..memory import Memory, MemoryProtection
from ..thread import Thread


# noinspection PyUnresolvedReferences
class ShellcodeInjectionMethod(ABC):
    _process: "Process"
    _memory: Memory

    def __init__(self, process: "Process"):
        self._process = process
        self._memory = Memory(process)

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class ShellcodeCreateRemoteThreadMethod(ShellcodeInjectionMethod):
    # noinspection PyUnresolvedReferences
    def execute(self, shellcode: bytes) -> Tuple["MemoryArea", Thread]:
        """
        Inject the shellcode and execute it using CreateRemoteThread.
        :param shellcode: the shellcode to inject
        :return: the shellcode memory area and the shellcode thread
        """
        area = self._memory.allocate_area(len(shellcode), MemoryProtection.PAGE_EXECUTE_READWRITE)
        area.write(shellcode)

        thread = self._process.create_thread(area.base_address)

        return area, thread
