from enum import IntEnum
from ctypes import Structure, c_int32

from .header_struct import HeaderStruct

__all__ = [
    "DriverStruct",
    "DriverResultStruct",
    "DriverResultStatus",
]


class DriverResultStatus(IntEnum):
    DRIVER_OK = 0
    DRIVER_INVALID_OR_CORRUPTED_HEADER = 1

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}.{self.name}"


class DriverStruct(Structure):
    _fields_ = [
        ("header", HeaderStruct),
        ("fd", c_int32),
    ]


class DriverResultStruct(Structure):
    _fields_ = [
        ("driver", DriverStruct),
        ("status", c_int32),
    ]
