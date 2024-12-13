import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
from src.city_collector import CityCollector


@pytest.mark.asyncio
async def test_fetch_cities_success():
    mock_json = [{'id': 1, 'nome': 'TestCity', 'microrregiao': {
        'mesorregiao': {'UF': {'sigla': 'TS'}}}}]

    with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_json)
        mock_get.return_value = mock_response

        cities = await CityCollector.fetch_cities()

        mock_get.assert_awaited_once_with(CityCollector.API_URL)
        mock_response.json.assert_awaited_once()
        assert cities == mock_json


@pytest.mark.asyncio
async def test_fetch_cities_failure():
    with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_get.return_value = mock_response

        with pytest.raises(Exception) as excinfo:
            await CityCollector.fetch_cities()

        mock_get.assert_awaited_once_with(CityCollector.API_URL)
        assert "Failed to fetch cities: 404" in str(excinfo.value)


@pytest.mark.asyncio
async def test_fetch_cities_network_error():
    with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = aiohttp.ClientError("Network error")

        with pytest.raises(aiohttp.ClientError) as excinfo:
            await CityCollector.fetch_cities()

        mock_get.assert_awaited_once_with(CityCollector.API_URL)
        assert "Network error" in str(excinfo.value)
