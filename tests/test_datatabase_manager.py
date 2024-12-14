import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, AsyncSession
from sqlalchemy.sql import select, text
from src.database_manager import DatabaseManager
from src.models import Municipio


@pytest.fixture
def db_manager():
    with patch(
        "src.database_manager.create_async_engine", new_callable=AsyncMock
    ) as mock_engine:
        with patch(
            "src.database_manager.sessionmaker", new_callable=AsyncMock
        ) as mock_sessionmaker:
            mock_engine.return_value = AsyncMock(spec=AsyncEngine)
            mock_sessionmaker.return_value = AsyncMock(spec=AsyncSession)
            db_manager = DatabaseManager()
            yield db_manager


@pytest.mark.asyncio
async def test_initialize(db_manager):
    mock_engine = db_manager.engine
    mock_conn = AsyncMock(spec=AsyncConnection)
    mock_engine.connect.return_value = mock_conn

    await db_manager.initialize()

    mock_engine.connect.assert_awaited_once()
    mock_conn.execute.assert_awaited_with(text("PRAGMA journal_mode = WAL"))
    mock_conn.run_sync.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_city(db_manager):
    city = MagicMock(spec=Municipio)
    mock_session = AsyncMock()
    db_manager.Session.return_value = mock_session

    await db_manager.add_city(city)

    mock_session.add.assert_called_once_with(city)
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_awaited()

    mock_session.commit.side_effect = Exception("Test Exception")
    with pytest.raises(RuntimeError) as excinfo:
        await db_manager.add_city(city)
    assert "Failed to add city to database" in str(excinfo.value)
    mock_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_cities(db_manager):
    mock_conn = AsyncMock(spec=AsyncConnection)
    db_manager.engine.begin.return_value = mock_conn
    mock_result = AsyncMock()
    mock_conn.execute.return_value = mock_result
    mock_result.scalars.return_value.all.return_value = [MagicMock(spec=Municipio)]

    result = await db_manager.get_all_cities()

    mock_conn.execute.assert_awaited_with(select(Municipio))
    mock_result.scalars.assert_called_once()
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_city_by_id(db_manager):
    mock_conn = AsyncMock(spec=AsyncConnection)
    db_manager.engine.begin.return_value = mock_conn
    mock_result = AsyncMock()
    mock_conn.execute.return_value = mock_result
    mock_result.scalar_one_or_none.return_value = MagicMock(spec=Municipio)

    city = await db_manager.get_city_by_id(1)

    mock_conn.execute.assert_awaited_with(select(Municipio).filter(Municipio.id == 1))
    mock_result.scalar_one_or_none.assert_called_once()
    assert city is not None


@pytest.mark.asyncio
async def test_close(db_manager):
    await db_manager.close()
    db_manager.engine.dispose.assert_awaited_once()
