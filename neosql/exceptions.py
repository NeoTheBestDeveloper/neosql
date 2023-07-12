__all__ = [
    "UseInvalidConnection",
]


class UseInvalidConnection(Exception):
    pass


class InvalidOrCorruptedHeader(Exception):
    pass
