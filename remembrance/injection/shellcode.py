from abc import ABC, abstractmethod

from remembrance.memory import Memory, MemoryProtection


class ShellcodeInjectionMethod(ABC):
    _memory: Memory

    # noinspection PyUnresolvedReferences
    def __init__(self, process: "Process"):
        self._memory = Memory(process)

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class ShellcodeCreateRemoteThreadMethod(ShellcodeInjectionMethod):
    def execute(self, shellcode: bytes):
        """
        Load the shellcode using CreateRemoteThread.
        :param shellcode: the shellcode to inject
        :return: the shellcode memory area and the shellcode thread
        """
        shellcode_area = self._memory.allocate_area(len(shellcode), MemoryProtection.PAGE_EXECUTE_READWRITE)
        shellcode_area.write(shellcode)

        thread = self._memory.process.create_thread(shellcode_area.base_address)

        return shellcode_area, thread
