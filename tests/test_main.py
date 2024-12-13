import pytest
from colorama import Fore, Style, init
from unittest.mock import AsyncMock, patch, MagicMock
from src.main import Main

init(autoreset=True)


@pytest.fixture
def main_instance():
    with patch('src.main.DatabaseManager') as mock_db_manager:
        with patch('src.main.CityDataScraper') as mock_scraper:
            mock_db_manager.return_value = AsyncMock()
            mock_scraper.return_value = AsyncMock()
            main = Main(verbose=True)
            yield main

# Test initialization


def test_init(main_instance):
    assert isinstance(main_instance.db, AsyncMock)
    assert isinstance(main_instance.city_scraper, AsyncMock)
    assert main_instance.verbose is True

# Test logging method


@pytest.mark.parametrize("level, color", [
    ("info", Fore.GREEN),
    ("warning", Fore.YELLOW),
    ("error", Fore.RED)
])
def test_log(main_instance, level, color, capsys):
    main_instance.log("Test message", level=level)
    captured = capsys.readouterr()

    assert color in captured.out
    expected_prefix = f"{color}[{level.upper()}] {Style.RESET_ALL}"
    assert f"{expected_prefix}Test message" in captured.out

# Test process_city for a new city


@pytest.mark.asyncio
async def test_process_city_new_city(main_instance):
    city_data = {
        'nome': 'TestCity',
        'microrregiao': {'mesorregiao': {'UF': {'sigla': 'TS'}}},
        'id': 1
    }
    mock_db = main_instance.db
    mock_db.get_city_by_id.return_value = None
    mock_db.add_city = AsyncMock()
    mock_scraper = main_instance.city_scraper
    mock_scraper.fetch_city_data = AsyncMock(
        return_value=(10000, 50000))

    with patch('src.main.print') as mock_print:
        await main_instance.process_city(city_data)
        mock_db.add_city.assert_called_once()
        mock_print.assert_any_call(f"{Fore.GREEN}[INFO] {
                                   Style.RESET_ALL}Processing city: TestCity/TS (ID: 1)")
        mock_print.assert_any_call(f"{Fore.GREEN}[INFO] {
                                   Style.RESET_ALL}Saved: TestCity/TS - Pop: 10000, PIB: 50000")

# Test process_city when city exists


@pytest.mark.asyncio
async def test_process_city_existing_city(main_instance):
    city_data = {
        'nome': 'TestCity',
        'microrregiao': {'mesorregiao': {'UF': {'sigla': 'TS'}}},
        'id': 1
    }
    mock_db = main_instance.db
    mock_db.get_city_by_id.return_value = MagicMock()

    with patch('src.main.print') as mock_print:
        await main_instance.process_city(city_data)
        mock_print.assert_any_call(f"{Fore.GREEN}[INFO] {
                                   Style.RESET_ALL}City already exists: TestCity/TS (ID: 1)")

# Test run method (very basic test due to complexity)


@pytest.mark.asyncio
async def test_run(main_instance):
    with patch('src.main.CityCollector.fetch_cities', new_callable=AsyncMock) as mock_fetch_cities:
        mock_fetch_cities.return_value = []
        await main_instance.run()
        mock_fetch_cities.assert_called_once()
        main_instance.db.initialize.assert_awaited_once()
        main_instance.db.close.assert_awaited_once()
