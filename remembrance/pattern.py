import re


class Pattern:
    __pattern: int
    __mask: int
    __byteorder: str

    @property
    def pattern(self) -> int:
        """ The pattern bytes. """
        return self.__pattern

    @property
    def mask(self) -> int:
        """ The pattern mask. """
        return self.__mask

    @property
    def byteorder(self) -> str:
        """ The pattern byte order. """
        return self.__byteorder

    @property
    def size(self) -> int:
        """ The pattern size in bytes. """
        return self.__mask.bit_length() // 8

    def __init__(self, pattern: int, mask: int, little_endian: bool):
        self.__pattern = pattern
        self.__mask = mask
        self.__byteorder = 'little' if little_endian else 'big'

    @staticmethod
    def compile(pattern: str, little_endian: bool = False) -> "Pattern":
        """
        Compile the pattern into a Pattern object.
        :param pattern: the pattern
        :param little_endian: if it's little endian or not
        :return: the compiled pattern
        """
        pattern = pattern.upper()
        pattern = re.sub(r'[^0-9A-F?]', '', pattern)
        pattern = ''.join(a + b for a, b in zip(pattern[::2], pattern[1::2]))

        mask = re.sub(r'[0-9A-F]', '1111', pattern)
        mask = re.sub(r'\?', '0000', mask)
        mask = int(mask, base=2)

        pattern = re.sub(r'\?', '0', pattern)
        pattern = int(pattern, base=16)

        return Pattern(pattern, mask, little_endian)

    def match_full(self, data: bytes) -> bool:
        """
        Check if the provided data matches the pattern.
        The data size must be the same as the pattern size.
        :param data: the data to check
        :return: if the pattern matches
        """
        masked_data = int.from_bytes(data, byteorder=self.__byteorder) & self.__mask
        return masked_data == self.__pattern

    def match(self, data: bytes) -> int:
        """
        Check if the provided data matches the pattern.
        It traverses the full buffer to match it.
        :param data: the data to check
        :return: the data offset
        """
        for offset in range(len(data) - self.size):
            if self.match_full(data[offset:offset + self.size]):
                return offset

        # noinspection PyTypeChecker
        return None

    def __str__(self) -> str:
        return f"Pattern(pattern={self.__pattern:#x}, mask={self.__mask:#x}, byteorder={self.__byteorder})"

    def __repr__(self) -> str:
        return self.__str__()
