from sys import platform
from pathlib import Path
from typing import Any, NoReturn
from ctypes import CDLL, POINTER, c_int32

from ..utils import SingletonMeta
from .structs import DriverResultStruct, DriverStruct

__all__ = [
    "NeosqlCore",
]


class NeosqlCore(metaclass=SingletonMeta):
    """Wrapper under CDDL c shared library."""

    _clib: CDLL
    _path: Path

    def __init__(self) -> None:
        self._init_lib_path()
        self._load()

    def _load(self) -> None | NoReturn:
        """Try to find and load c shared library."""
        if not self._path.exists():
            raise FileNotFoundError(f"Cannot load neosql-core by '{self._path.absolute().as_posix()}' path.")

        self._clib = CDLL(self._path.absolute().as_posix())

        self._init_ffi_functions()

        return None

    def _init_lib_path(self) -> None | NoReturn:
        """Get library path dependent on users platform."""
        if platform.startswith(("linux", "darwin")):
            self._path = Path(__file__).parent.joinpath("_neosql_core.so")
        elif platform.startswith("win32"):
            self._path = Path(__file__).parent.joinpath("_neosql_core.dll")
        else:
            raise OSError(f"This platform '{platform}' is not supported.")

        return None

    def _init_ffi_functions(self) -> None:
        """Set signatures for C functions from shared library."""
        self._clib.driver_create_db.restype = DriverStruct
        self._clib.driver_create_db.argtypes = (c_int32,)

        self._clib.driver_open_db.restype = DriverResultStruct
        self._clib.driver_open_db.argtypes = (c_int32,)

        self._clib.driver_free.argtypes = (POINTER(DriverStruct),)
        self._clib.driver_free.restype = None

    def __getattribute__(self, __name: str) -> Any:
        """If attribute is FuncPointer return it from _clib."""
        if __name == "_clib":
            return object.__getattribute__(self, __name)

        clib = getattr(self, "_clib", None)

        if clib is not None:
            clib_attr = getattr(clib, __name, None)

            if issubclass(type(clib_attr), clib._FuncPtr):
                return clib_attr

        return object.__getattribute__(self, __name)
