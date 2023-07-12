from typing import TYPE_CHECKING
from ctypes import pointer, _Pointer

from ..neosql_core import NeosqlCore
from ..structs import DriverResultStruct, DriverStruct

__all__ = [
    "DriverMethods",
]

if TYPE_CHECKING:
    DriverStructPointer = _Pointer[DriverStruct]
else:
    DriverStructPointer = pointer


class DriverMethods:
    """Object for accessing driver methods from C library with python typing."""

    _clib: NeosqlCore

    def __init__(self) -> None:
        self._clib = NeosqlCore()

    def create_db(self, fd: int) -> DriverStruct:
        return self._clib.driver_create_db(fd)

    def open_db(self, fd: int) -> DriverResultStruct:
        return self._clib.driver_open_db(fd)

    def free(self, driver: DriverStructPointer) -> None:
        self._clib.driver_free(driver)
