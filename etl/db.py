from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from .config import DB_URL

_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(DB_URL)
    return _engine
