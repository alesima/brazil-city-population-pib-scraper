import aiohttp


class CityCollector:
    API_URL = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'

    @classmethod
    async def fetch_cities(cls) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.API_URL) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to fetch cities: {
                                    response.status}")
