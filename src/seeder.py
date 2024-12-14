import asyncio
import aiohttp
from colorama import init
from .database_manager import DatabaseManager
from .city_collector import CityCollector
from .city_data_scraper import CityDataScraper
from .models import Municipio
from .utils import log

init(autoreset=True)


class Seeder:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.db = DatabaseManager(
            db_url='sqlite+aiosqlite:///municipios.db')
        self.city_scraper = CityDataScraper()

    async def process_city(self, city_data: dict):
        city_name = city_data['nome']
        state_code = city_data['microrregiao']['mesorregiao']['UF']['sigla']
        city_id = city_data['id']

        city = await self.db.get_city_by_id(id=city_id)

        if city is not None:
            log(f"City already exists: {
                city_name}/{state_code} (ID: {city_id})")
            return

        log(f"Processing city: {
            city_name}/{state_code} (ID: {city_id})")

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=100, limit=1000)) as session:
            try:
                population, pib_per_capita = await self.city_scraper.fetch_city_data(session, city_name, state_code)
            except Exception as e:
                log(f"Error processing city {
                    city_name}/{state_code}: {str(e)}", level="error")
                return

        if population is None or pib_per_capita is None:
            log(f"Failed to fetch data for {
                city_name}/{state_code}", level="warning")
            return

        city = Municipio(
            id=city_id,
            nome=city_name,
            estado=state_code,
            populacao=population,
            pib_per_capita=pib_per_capita
        )

        await self.db.add_city(city)
        log(f"Saved: {
            city_name}/{state_code} - Pop: {population}, PIB: {pib_per_capita}", level="info")

    async def run(self):
        log("Initializing database...", level="info")

        await self.db.initialize()

        log("Database initialized.", level="info")

        log("Fetching cities from IBGE API...", level="info")

        cities = await CityCollector.fetch_cities()

        log(f"Fetched {len(cities)} cities from IBGE API.")

        tasks = [self.process_city(city) for city in cities]
        await asyncio.gather(*tasks)

        await self.db.close()
        log("Completed processing all cities.", level="info")


