from ctypes import pointer

from .methods import DriverMethods
from ..exceptions import InvalidOrCorruptedHeader
from .structs import DriverStruct, DriverResultStatus

__all__ = [
    "Driver",
]


class Driver:
    """High level wrapper under database driver which written in C."""

    _cdriver: DriverStruct
    _cmethods: DriverMethods

    def __init__(self, fd: int, create_db: bool = False) -> None:
        self._cmethods = DriverMethods()

        if create_db:
            self._cdriver = self._cmethods.create_db(fd)
        else:
            driver_res = self._cmethods.open_db(fd)

            if driver_res.status == DriverResultStatus.DRIVER_INVALID_OR_CORRUPTED_HEADER:
                raise InvalidOrCorruptedHeader
            self._cdriver = driver_res.driver

    def close(self) -> None:
        """Free all heap allocated my driver memory, don't close database fd."""
        self._cmethods.free(pointer(self._cdriver))
