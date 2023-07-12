import os
from pathlib import Path
from functools import wraps
from typing import LiteralString, Self

from .exceptions import UseInvalidConnection
from .ffi import Driver

__all__ = [
    "Connection",
]


def check_alive(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        if not self.alive:
            raise UseInvalidConnection("Use not alive connection.")
        return method(self, *method_args, **method_kwargs)

    return _impl


class Connection:
    _fd: int
    _path: Path
    _is_alive: bool
    _driver: Driver

    def __init__(self, path: Path | str) -> None:
        self._is_alive = True
        self._path = Path(path)

        is_new_db = not self._path.exists()

        # Binary flags only used at windows because it translate '\n' -> '\n\r' that breaks database logic.
        O_BINARY = getattr(os, "O_BINARY", 0)
        db_file_flags = os.O_CREAT | os.O_RDWR | O_BINARY

        self._fd = os.open(self._path.absolute(), db_file_flags)
        self._driver = Driver(self._fd, create_db=is_new_db)

    @check_alive
    def close(self) -> None:
        self._driver.close()
        os.close(self._fd)
        self._is_alive = False

    @check_alive
    def get_db_info(self) -> "DatabaseInfo":
        ...

    @check_alive
    def get_table_info(self, name: str) -> "TableInfo":
        ...

    @check_alive
    def exec(self, statement: LiteralString) -> None:
        ...

    @property
    def alive(self) -> bool:
        return self._is_alive

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        self.close()
