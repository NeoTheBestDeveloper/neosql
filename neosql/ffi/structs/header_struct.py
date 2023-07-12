from enum import IntEnum
from typing import NoReturn, Self
from ctypes import Structure, c_int32

from .addr_struct import AddrStruct


__all__ = [
    "StorageType",
    "HeaderStruct",
]


class StorageType(IntEnum):
    STORAGE_TYPE_LIST = 0
    STORAGE_TYPE_BTREE = 1

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}.{self.name}"


class HeaderStruct(Structure):
    _fields_ = [
        ("first_table", AddrStruct),
        ("last_table", AddrStruct),
        ("pages_count", c_int32),
        ("storage_type", c_int32),
    ]

    def __eq__(self, other: Self) -> bool | NoReturn:
        if not issubclass(type(other), HeaderStruct):
            return NotImplemented
        return (
            self.pages_count == other.pages_count
            and self.storage_type == other.storage_type
            and self.first_table == other.first_table
            and self.last_table == other.last_table
        )
