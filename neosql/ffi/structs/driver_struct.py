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

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}.{self.name}"


class DriverStruct(Structure):
    _fields_ = [
        ("_header", HeaderStruct),
        ("_fd", c_int32),
    ]

    def __init__(self, header: HeaderStruct, fd: int) -> None:
        super().__init__(header, int)

    @property
    def header(self) -> HeaderStruct:
        return self._header

    @property
    def fd(self) -> int:
        return self._fd

    def __repr__(self) -> str:
        return f"Driver(\n\theader={self.header},\n\tfd={self.fd}\n)"


class DriverResultStruct(Structure):
    _fields_ = [
        ("_driver", DriverStruct),
        ("_status", c_int32),
    ]

    def __init__(self, driver: DriverStruct, status: DriverResultStatus) -> None:
        super().__init__(driver, status)

    @property
    def driver(self) -> DriverStruct:
        return self._driver

    @property
    def status(self) -> DriverResultStatus:
        return DriverResultStatus(self._status)

    def __repr__(self) -> str:
        return f"DriverResult(\ndriver={self.driver},\nstatus={self.status}\n)"
