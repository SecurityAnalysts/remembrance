import ctypes
import enum
from ctypes.wintypes import DWORD

from .native import Kernel32
from .native.exception import WinAPIException
from .native.structure import MEMORY_BASIC_INFORMATION
from .pattern import Pattern


class MemoryAllocationType(enum.IntEnum):
    MEM_COMMIT = 0x00001000
    MEM_RESERVE = 0x00002000
    MEM_RESET = 0x00080000
    MEM_RESET_UNDO = 0x1000000

    MEM_LARGE_PAGES = 0x20000000
    MEM_PHYSICAL = 0x00400000
    MEM_TOP_DOWN = 0x00100000


class MemoryProtection(enum.IntEnum):
    PAGE_EXECUTE = 0x10
    PAGE_EXECUTE_READ = 0x20
    PAGE_EXECUTE_READWRITE = 0x40
    PAGE_EXECUTE_WRITECOPY = 0x80
    PAGE_NOACCESS = 0x01
    PAGE_READONLY = 0x02
    PAGE_READWRITE = 0x04
    PAGE_WRITECOPY = 0x08
    PAGE_TARGETS_INVALID = 0x40000000
    PAGE_TARGETS_NO_UPDATE = 0x40000000

    PAGE_GUARD = 0x100
    PAGE_NOCACHE = 0x200
    PAGE_WRITECOMBINE = 0x400


class MemoryFreeType(enum.IntEnum):
    MEM_DECOMMIT = 0x00004000
    MEM_RELEASE = 0x00008000

    MEM_COALESCE_PLACEHOLDERS = 0x00000001
    MEM_PRESERVE_PLACEHOLDER = 0x00000002


class MemoryArea:
    __memory: "Memory"
    __base_address: int
    __size: int

    @property
    def memory(self) -> "Memory":
        return self.__memory

    @property
    def base_address(self) -> int:
        return self.__base_address

    @property
    def size(self) -> int:
        return self.__size

    def __init__(self, memory: "Memory", base_address: int, size: int):
        self.__memory = memory
        self.__base_address = base_address
        self.__size = size

    def write(self, data: bytes, offset: int = 0):
        """
        Write some data to the memory area.
        :param data: the data to write
        :param offset: the offset to write at
        """
        self.__memory.write(self.__base_address + offset, data)

    def read(self, offset: int = 0, size: int = None):
        """
        Read some data from the memory area.
        :param offset: the offset to read from
        :param size: how many bytes to read (memory area size if None)
        :return: the read data
        """
        if size is None:
            size = self.__size

        return self.__memory.read(self.__base_address + offset, size)

    def free(self, *args, **kwargs):
        """
        Free the memory area.
        NOTE: For more parameters, look at Memory.free documentation.
        """
        self.__memory.free(self.__base_address, self.__size, *args, **kwargs)

    def protect(self, protection: MemoryProtection) -> MemoryProtection:
        """
        Change the memory area protection.
        :param protection: the new memory area protection
        :return: the old memory area protection
        """
        return self.__memory.protect(self.__base_address, self.__size, protection)

    def __str__(self) -> str:
        return f"MemoryArea(memory={self.__memory}, base_address={self.__base_address:#x}, size={self.__size})"

    def __repr__(self) -> str:
        return self.__str__()


class Memory:
    # noinspection PyUnresolvedReferences
    __process: "Process"

    # noinspection PyUnresolvedReferences
    @property
    def process(self) -> "Process":
        return self.__process

    # noinspection PyUnresolvedReferences
    def __init__(self, process: "Process"):
        self.__process = process

    def write(self, address: int, data: bytes):
        """
        Write some data into the memory.
        :param address: the address to write to
        :param data: the data to write
        """
        if not Kernel32.WriteProcessMemory(self.__process.handle.native, address, data, len(data), None):
            raise WinAPIException

    def read(self, address: int, size: int) -> bytes:
        """
        Read some data from the memory.
        :param address: the address to read from
        :param size: how many bytes to read
        :return: the read data
        """
        buffer = ctypes.create_string_buffer(size)
        if not Kernel32.ReadProcessMemory(self.__process.handle.native, address, buffer, size, None):
            raise WinAPIException

        return buffer.raw

    def allocate(self, size: int, protection: MemoryProtection,
                 allocation_type: MemoryAllocationType = MemoryAllocationType.MEM_COMMIT) -> int:
        """
        Allocate some memory.
        :param size: how many bytes to allocate
        :param protection: the memory protection
        :param allocation_type: the allocation type
        :return: the address of the newly allocated memory
        """
        address = Kernel32.VirtualAllocEx(self.__process.handle.native, None, size, allocation_type, protection)
        if address is None:
            raise WinAPIException

        return address

    def allocate_area(self, size: int, protection: MemoryProtection, *args, **kwargs) -> MemoryArea:
        """
        Allocate a memory area.
        NOTE: For more parameters, look at Memory.allocate documentation.
        :param size: how many bytes to allocate
        :param protection: the memory protection
        :return: the MemoryArea object
        """
        return MemoryArea(self, self.allocate(size, protection, *args, **kwargs), size)

    def free(self, address: int, size: int, free_type: MemoryFreeType):
        """
        Free some previously allocated memory.
        :param address: the memory address
        :param size: the memory size
        :param free_type: the free type
        """
        if not Kernel32.VirtualFreeEx(self.__process.handle.native, address, size, free_type):
            raise WinAPIException

    def protect(self, address: int, size: int, protection: MemoryProtection) -> MemoryProtection:
        """
        Change the protection of some allocated memory.
        :param address: the memory address
        :param size: the memory size
        :param protection: the new protection
        :return: the old protection
        """
        old_protection = DWORD()
        if not Kernel32.VirtualProtectEx(self.__process.handle.native, address, size, protection,
                                         ctypes.pointer(old_protection)):
            raise WinAPIException

        return MemoryProtection(old_protection.value)

    def scan(self, pattern: Pattern, address: int, size: int) -> int:
        memory_info = MEMORY_BASIC_INFORMATION()

        if not Kernel32.VirtualQueryEx(self.process.handle.native, address, ctypes.pointer(memory_info),
                                       ctypes.sizeof(MEMORY_BASIC_INFORMATION)):
            raise WinAPIException

        current = address
        while current < address + size:
            if not Kernel32.VirtualQueryEx(self.process.handle.native, current,
                                           ctypes.pointer(memory_info), ctypes.sizeof(MEMORY_BASIC_INFORMATION)):
                continue

            if memory_info.State != MemoryAllocationType.MEM_COMMIT or (memory_info.Protect ==
                                                                        MemoryProtection.PAGE_NOACCESS):
                continue

            old_protection = self.protect(memory_info.BaseAddress, memory_info.RegionSize,
                                          MemoryProtection.PAGE_EXECUTE_READWRITE)

            buffer = self.read(memory_info.BaseAddress, memory_info.RegionSize)
            self.protect(memory_info.BaseAddress, memory_info.RegionSize, old_protection)

            offset = pattern.match(buffer)
            if offset is not None:
                return offset

            current += memory_info.RegionSize

    def __str__(self) -> str:
        return f"Memory(process={self.__process})"

    def __repr__(self) -> str:
        return self.__str__()
