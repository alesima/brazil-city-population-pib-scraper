import re
import requests
from bs4 import BeautifulSoup
from .utils import slugify


class CityDataScraper:
    BASE_URL = 'https://www.ibge.gov.br/cidades-e-estados'

    def _extract_number(self, text: str):
        """Extract a number from a string, removing formatting."""
        return int(re.sub(r'\D', '', text))

    def _extract_float(self, text: str):
        """Convert a text into a float after sanitizing unwanted characters."""
        # Remove unwanted characters like '\xa0' and anything inside square brackets
        sanitized_text = re.sub(
            r'\[.*?\]', '', text).replace('\xa0', '').strip()
        return float(sanitized_text.replace('R$', '').replace('.', '').replace(',', '.'))

    async def fetch_city_data(self, session, city_name: str, state_code: str):
        """Fetch population and PIB per capita for a city."""
        url = f'{self.BASE_URL}/{state_code.lower()
                                 }/{slugify(city_name)}.html'
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch data for {city_name}, {state_code}")
            return None, None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize data
        population = None
        pib_per_capita = None

        # Iterate over all div.indicador elements
        indicators = soup.find_all('div', class_='indicador')
        for indicator in indicators:
            label = indicator.find('p')  # Get the label text inside <p>

            # Match population
            if label and 'População residente' in label.text:
                ind_value = indicator.find('p', class_='ind-value')
                if ind_value.find('small'):
                    ind_value.find('small').decompose()  # Remove small tag
                population_text = ind_value.get_text(separator=' ', strip=True)

                # Validate and parse population
                try:
                    population = self._extract_number(population_text)
                except ValueError:
                    print(f"Invalid population value for {
                          city_name}, {state_code}: {population_text}")

            # Match PIB per capita
            elif label and 'PIB per capita' in label.text:
                pib_text = indicator.find('p', class_='ind-value').text.strip()

                # Validate and parse PIB per capita
                try:
                    pib_per_capita = self._extract_float(pib_text)
                except ValueError:
                    print(f"Invalid PIB value for {
                          city_name}, {state_code}: {pib_text}")

        # Ensure valid data is returned
        if population is None or pib_per_capita is None:
            print(f"Incomplete data for {city_name}, {
                  state_code}. Population: {population}, PIB: {pib_per_capita}")

        return population, pib_per_capita
