from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from database import async_session_factory
from db.models import Client


async def add_user(id: int, number: str, username: str, car_type: str):
    async with async_session_factory() as session:
        user: Client = Client(id=id, number=number, telegram=username, is_auto=int(car_type))
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def get_phone(id_user: int):
    async with async_session_factory() as session:
        query = select(Client.number).where(Client.id == id_user)
        result = await session.execute(query)
        number = result.scalar_one_or_none()
    if number:
        return number


async def check_user(id_user: int):
    async with async_session_factory() as session:
        query = select(func.count(Client.id)).where(Client.id == id_user)
        result = await session.execute(query)
        number = result.scalar_one_or_none()
    if number == 1:
        return True
    else:
        return False
