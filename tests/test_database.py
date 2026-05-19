from alphasignal_shared.database import create_engine, create_session_factory
from sqlalchemy.ext.asyncio import AsyncEngine


def test_create_engine_and_session_factory() -> None:
    engine = create_engine("sqlite+aiosqlite:///:memory:")
    session_factory = create_session_factory(engine)

    assert isinstance(engine, AsyncEngine)
    assert session_factory is not None
