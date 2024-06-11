from aiohttp import ClientSession
from settings.db_config import API_KEY

translator = {'Фамилия': 'surname',
              'Имя': 'name',
              'Отчество': 'patronymic',
              'Номертелефона': 'phone_number',
              'Telegram': 'telegram'}


async def prepare_data(data: str) -> str:
    parsed_data: str = data.replace('\n', '').replace(' ', '')
    return parsed_data


async def parse_driver_data(data: str) -> dict:
    parsed_data: str = await prepare_data(data)
    lines: list[str] = parsed_data.split(',')
    driver_data = {}

    for line in lines:
        if line:
            key, value = line.split(':')
            driver_data[translator[key]] = value
    return driver_data


async def get_coordinates(query: str):
    url: str = f"https://api.geoapify.com/v1/geocode/search?text={query}&apiKey={API_KEY}"
    async with ClientSession() as session:
        async with session.get(url=url, headers={"Accept": "application/json"}) as response:
            return await response.json()


async def get_distance(coordinates: tuple[tuple[int, int], tuple[int, int]]):
    url: str = (f"https://api.geoapify.com/v1/routing?waypoints={coordinates[0][0]}%2C{coordinates[0][1]}%7C"
                f"{coordinates[1][0]}%2C{coordinates[1][1]}&mode=drive&apiKey={API_KEY}")
    print(url)
    async with ClientSession() as session:
        async with session.get(url=url, headers={"Accept": "application/json"}) as response:
            return await response.json()



