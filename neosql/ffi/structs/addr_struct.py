from typing import NoReturn, Self
from ctypes import Structure, c_int16, c_int32

__all__ = [
    "AddrStruct",
]


class AddrStruct(Structure):
    _fields_ = [
        ("_page_id", c_int32),
        ("_offset", c_int16),
    ]

    def __init__(self, page_id: int, offset: int) -> None:
        super().__init__(page_id, offset)

    @property
    def page_id(self) -> int:
        return self._page_id

    @property
    def offset(self) -> int:
        return self._offset

    def __repr__(self) -> str:
        return f"Addr(page_id={self.page_id}, offset={self.offset})"

    def __eq__(self, other: Self) -> bool | NoReturn:
        if not issubclass(type(other), AddrStruct):
            return NotImplemented

        return self.page_id == other.page_id and self.offset == other.offset
