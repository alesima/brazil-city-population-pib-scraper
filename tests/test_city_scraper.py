import pytest
import aiohttp
from unittest.mock import patch, MagicMock, AsyncMock
from bs4 import BeautifulSoup
from src.city_data_scraper import CityDataScraper


@pytest.fixture
def scraper():
    return CityDataScraper()


def test_extract_number(scraper):
    assert scraper._extract_number("1.234.567") == 1234567
    assert scraper._extract_number("1,234,567") == 1234567
    assert scraper._extract_number("1,234.567") == 1234567
    assert scraper._extract_number("1.234,567") == 1234567
    assert scraper._extract_number("R$1,234,567") == 1234567


def test_extract_float(scraper):
    assert scraper._extract_float("R$ 1.234,56") == 1234.56
    assert scraper._extract_float("1.234,56") == 1234.56
    assert scraper._extract_float("R$1.234,56 [abc]") == 1234.56
    assert scraper._extract_float("1,234.56\xa0") == 1234.56


@patch("aiohttp.ClientSession.get")
@patch("src.city_data_scraper.BeautifulSoup")
@pytest.mark.asyncio
async def test_fetch_city_data_success(mock_soup, mock_get, scraper):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(
        return_value='<html><div class="indicador"><p>População residente</p><p class="ind-value">1.234.567</p></div><div class="indicador"><p>PIB per capita</p><p class="ind-value">R$ 12.345,67</p></div></html>'
    )
    mock_get.return_value.__aenter__.return_value = mock_response
    mock_soup.return_value.find_all.return_value = [
        BeautifulSoup(
            '<div class="indicador"><p>População residente</p><p class="ind-value">1.234.567</p></div>',
            "html.parser",
        ).find("div", class_="indicador"),
        BeautifulSoup(
            '<div class="indicador"><p>PIB per capita</p><p class="ind-value">R$ 12.345,67</p></div>',
            "html.parser",
        ).find("div", class_="indicador"),
    ]

    async with aiohttp.ClientSession() as session:
        population, pib_per_capita = await scraper.fetch_city_data(
            session, "TestCity", "TS"
        )

    assert population == 1234567
    assert pib_per_capita == 12345.67
    mock_get.assert_called_once_with(
        "https://www.ibge.gov.br/cidades-e-estados/ts/testcity.html"
    )


@patch("aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_fetch_city_data_failure(mock_get, scraper):
    mock_response = MagicMock()
    mock_response.status = 404
    mock_get.return_value.__aenter__.return_value = mock_response

    async with aiohttp.ClientSession() as session:
        population, pib_per_capita = await scraper.fetch_city_data(
            session, "TestCity", "TS"
        )

    assert population is None
    assert pib_per_capita is None
    mock_get.assert_called_once_with(
        "https://www.ibge.gov.br/cidades-e-estados/ts/testcity.html"
    )


@patch("aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_fetch_city_data_network_error(mock_get, scraper):
    mock_get.side_effect = aiohttp.ClientError("Network Error")

    async with aiohttp.ClientSession() as session:
        population, pib_per_capita = await scraper.fetch_city_data(
            session, "TestCity", "TS"
        )

    assert population is None
    assert pib_per_capita is None
