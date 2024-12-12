import argparse
import asyncio
import aiohttp
from colorama import Fore, Style, init
from .database_manager import DatabaseManager
from .city_collector import CityCollector
from .city_data_scraper import CityDataScraper
from .models import Municipio

init(autoreset=True)


class Main:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.db_manager = DatabaseManager()
        self.city_scraper = CityDataScraper()

    def log(self, message, level="info"):
        """Log messages with color depending on the level."""
        if self.verbose:
            if level == "info":
                print(f"{Fore.GREEN}[INFO] {Style.RESET_ALL}{message}")
            elif level == "warning":
                print(f"{Fore.YELLOW}[WARNING] {Style.RESET_ALL}{message}")
            elif level == "error":
                print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{message}")

    async def process_city(self, city_data: dict):

        city_name = city_data['nome']
        state_code = city_data['microrregiao']['mesorregiao']['UF']['sigla']
        city_id = city_data['id']

        self.log(f"Processing city: {
            city_name}/{state_code} (ID: {city_id})")

        async with aiohttp.ClientSession() as session:
            population, pib_per_capita = self.city_scraper.fetch_city_data(session,
                                                                           city_name, state_code)

        if population is None or pib_per_capita is None:
            self.log(f"Failed to fetch data for {
                city_name}/{state_code}", level="warning")

        city = Municipio(
            id=city_id,
            nome=city_name,
            estado=state_code,
            populacao=population,
            pib_per_capita=pib_per_capita
        )

        self.db_manager.add_city(city)
        self.log(f"Saved: {
            city_name}/{state_code} - Pop: {population}, PIB: {pib_per_capita}", level="info")

        self.db_manager.close()
        self.log("Completed processing all cities.", level="info")

    async def run(self):
        city_collector = CityCollector()
        cities = city_collector.fetch_cities()

        self.log(f"Fetched {len(cities)} cities from IBGE API.")

        tasks = [self.process_city(city) for city in cities]
        await asyncio.gather(*tasks)

        self.db_manager.close()
        self.log("Completed processing all cities.", level="info")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="City Population and PIB Scraper")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose logging"
    )
    args = parser.parse_args()

    main = Main(verbose=args.verbose)
    asyncio.run(main.run())
