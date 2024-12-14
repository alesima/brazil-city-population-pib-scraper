import asyncio
from prompt_toolkit import prompt
from colorama import init
from .database_manager import DatabaseManager
from .utils import log

init(autoreset=True)


class Updater:
    def __init__(self):
        self.db = DatabaseManager(db_url='sqlite+aiosqlite:///municipios.db')

    async def get_user_input(self, prompt_message: str):
        return await asyncio.to_thread(prompt, prompt_message)

    async def search_and_select_city(self, city_name: str):
        results = await self.db.search_city(city_name)
        if len(results) == 0:
            log("Cidade não encontrada.", level="error")
            return None

        log("Escolha uma cidade:", level="info")
        for index, city in enumerate(results):
            log(f"{index + 1}: {city.nome}", level="info")

        index = int(await self.get_user_input("Escolha uma cidade: ")) - 1
        return results[index]

    async def update_city_fields(self, city):
        log(f"Atualizando cidade: {city.nome}", level="info")

        possui_cicc = int(await self.get_user_input("Possui CICC (0 para Não ou 1 para Sim): "))
        possui_gcm = int(await self.get_user_input("Possui GCM (0 para Não ou 1 para Sim): "))
        possui_samu = int(await self.get_user_input("Possui SAMU (0 para Não ou 1 para Sim): "))

        city.possui_cicc = possui_cicc
        city.possui_gcm = possui_gcm
        city.possui_samu = possui_samu

        await self.db.update_city(city)

    async def update_city(self):
        city_name = await self.get_user_input("Digite o nome da cidade: ")

        if not city_name:
            log("Nome da cidade inválido.", level="error")
            return

        city = await self.search_and_select_city(city_name)
        if city:
            await self.update_city_fields(city)

    async def run(self):
        await self.db.initialize()
        await self.update_city()
        await self.db.close()
