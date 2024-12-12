import requests


class CityCollector:
    API_URL = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'

    def fetch_cities(self):
        response = requests.get(self.API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch cities: {response.status_code}")
