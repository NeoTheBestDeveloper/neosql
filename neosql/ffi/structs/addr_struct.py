from typing import NoReturn, Self
from ctypes import Structure, c_int16, c_int32

__all__ = [
    "AddrStruct",
]


class AddrStruct(Structure):
    _fields_ = [
        ("page_id", c_int32),
        ("offset", c_int16),
    ]

    def __eq__(self, other: Self) -> bool | NoReturn:
        if not issubclass(type(other), AddrStruct):
            return NotImplemented

        return self.page_id == other.page_id and self.offset == other.offset
