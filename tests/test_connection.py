import shutil

import pytest

from neosql import Connection
from neosql.exceptions import InvalidOrCorruptedHeader, UseInvalidConnection
from neosql.ffi.structs.header_struct import HeaderStruct
from neosql.ffi.structs.addr_struct import AddrStruct
from neosql.ffi.structs.header_struct import StorageType

from . import ASSETS_PATH


@pytest.fixture()
def zero_db_content() -> bytes:
    with open(ASSETS_PATH / "zero_db.db", "rb") as fin:
        return fin.read()


def test_connection_create_db(tmp_path, zero_db_content):
    db_path = tmp_path / "database.db"
    conn = Connection(db_path)

    default_header = HeaderStruct(
        AddrStruct(-1, -1),
        AddrStruct(-1, -1),
        1,
        StorageType.STORAGE_TYPE_LIST,
    )

    assert conn.alive
    assert conn._path == db_path
    assert conn._driver._cdriver.fd == conn._fd
    assert conn._driver._cdriver.header == default_header

    conn.close()
    assert not conn.alive

    with open(db_path, "rb") as fin:
        assert fin.read() == zero_db_content


def test_connection_open_db(tmp_path):
    db_path = tmp_path / "database.db"
    shutil.copy(ASSETS_PATH / "tree_tables_db.db", db_path)
    conn = Connection(db_path)

    header = HeaderStruct(
        AddrStruct(0, 0),
        AddrStruct(0, 104),
        1,
        StorageType.STORAGE_TYPE_LIST,
    )

    assert conn.alive
    assert conn._path == db_path
    assert conn._driver._cdriver.fd == conn._fd
    assert conn._driver._cdriver.header == header

    conn.close()
    assert not conn.alive


def test_check_is_alive(tmp_path):
    db_path = tmp_path / "database.db"
    conn = Connection(db_path)
    conn.close()

    with pytest.raises(UseInvalidConnection):
        conn.close()

    with pytest.raises(UseInvalidConnection):
        conn.exec()

    with pytest.raises(UseInvalidConnection):
        conn.get_db_info()

    with pytest.raises(UseInvalidConnection):
        conn.get_table_info()


def test_open_invalid_db():
    for i in range(1, 4):
        with pytest.raises(InvalidOrCorruptedHeader):
            db_path = ASSETS_PATH / f"invalid_db_{i}.db"
            Connection(db_path)
