import pytest
from colorama import Fore, Style, init
from unittest.mock import AsyncMock, patch, MagicMock
from src.seeder import Seeder

init(autoreset=True)


@pytest.fixture
def seeder_instance():
    with patch('src.seeder.DatabaseManager') as mock_db_manager:
        with patch('src.seeder.CityDataScraper') as mock_scraper:
            mock_db_manager.return_value = AsyncMock()
            mock_scraper.return_value = AsyncMock()
            seeder = Seeder(verbose=True)
            yield seeder


def test_init(seeder_instance):
    assert isinstance(seeder_instance.db, AsyncMock)
    assert isinstance(seeder_instance.city_scraper, AsyncMock)
    assert seeder_instance.verbose is True


@pytest.mark.parametrize("level, color", [
    ("info", Fore.GREEN),
    ("warning", Fore.YELLOW),
    ("error", Fore.RED)
])
def test_log(seeder_instance, level, color, capsys):
    seeder_instance.log("Test message", level=level)
    captured = capsys.readouterr()

    assert color in captured.out
    expected_prefix = f"{color}[{level.upper()}] {Style.RESET_ALL}"
    assert f"{expected_prefix}Test message" in captured.out


@pytest.mark.asyncio
async def test_process_city_new_city(seeder_instance):
    city_data = {
        'nome': 'TestCity',
        'microrregiao': {'mesorregiao': {'UF': {'sigla': 'TS'}}},
        'id': 1
    }
    mock_db = seeder_instance.db
    mock_db.get_city_by_id.return_value = None
    mock_db.add_city = AsyncMock()
    mock_scraper = seeder_instance.city_scraper
    mock_scraper.fetch_city_data = AsyncMock(
        return_value=(10000, 50000))

    with patch('src.seeder.print') as mock_print:
        await seeder_instance.process_city(city_data)
        mock_db.add_city.assert_called_once()
        mock_print.assert_any_call(f"{Fore.GREEN}[INFO] {
                                   Style.RESET_ALL}Processing city: TestCity/TS (ID: 1)")
        mock_print.assert_any_call(f"{Fore.GREEN}[INFO] {
                                   Style.RESET_ALL}Saved: TestCity/TS - Pop: 10000, PIB: 50000")


@pytest.mark.asyncio
async def test_process_city_existing_city(seeder_instance):
    city_data = {
        'nome': 'TestCity',
        'microrregiao': {'mesorregiao': {'UF': {'sigla': 'TS'}}},
        'id': 1
    }
    mock_db = seeder_instance.db
    mock_db.get_city_by_id.return_value = MagicMock()

    with patch('src.seeder.print') as mock_print:
        await seeder_instance.process_city(city_data)
        mock_print.assert_any_call(f"{Fore.GREEN}[INFO] {
                                   Style.RESET_ALL}City already exists: TestCity/TS (ID: 1)")


@pytest.mark.asyncio
async def test_run(seeder_instance):
    with patch('src.seeder.CityCollector.fetch_cities', new_callable=AsyncMock) as mock_fetch_cities:
        mock_fetch_cities.return_value = []
        await seeder_instance.run()
        mock_fetch_cities.assert_called_once()
        seeder_instance.db.initialize.assert_awaited_once()
        seeder_instance.db.close.assert_awaited_once()
