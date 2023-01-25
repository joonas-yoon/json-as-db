from .core.database import Database


def load(path: str, *args, **kwargs) -> Database:
    return Database().load(path, *args, **kwargs)

