from enum import IntEnum
from functools import cached_property
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

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}.{self.name}"


class HeaderStruct(Structure):
    _fields_ = [
        ("_first_table", AddrStruct),
        ("_last_table", AddrStruct),
        ("_pages_count", c_int32),
        ("_storage_type", c_int32),
    ]

    def __init__(
        self, first_table: AddrStruct, last_table: AddrStruct, pages_count: int, storage_type: StorageType
    ) -> None:
        super().__init__(first_table, last_table, pages_count, storage_type)

    @property
    def first_table(self) -> AddrStruct:
        return self._first_table

    @property
    def last_table(self) -> AddrStruct:
        return self._last_table

    @property
    def pages_count(self) -> int:
        return self._pages_count

    @cached_property
    def storage_type(self) -> StorageType:
        return StorageType(self._storage_type)

    def __repr__(self) -> str:
        return f"Header(first_table={self.first_table}, last_table={self.last_table}, pages_count={self.pages_count}, storage_type={self.storage_type})"

    def __eq__(self, other: Self) -> bool | NoReturn:
        if not issubclass(type(other), HeaderStruct):
            return NotImplemented
        return (
            self.pages_count == other.pages_count
            and self.storage_type == other.storage_type
            and self.first_table == other.first_table
            and self.last_table == other.last_table
        )
