from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from db.models import Driver
from database import async_session_factory
from settings.admin import admin_tg


async def check_admin(id: int) -> bool:
    if id in admin_tg:
        return True
    return False


async def add_driver(driver_data: dict):
    async with async_session_factory() as session:
        driver = Driver(**driver_data)
        session.add(driver)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def get_driver_data(driver_id: int) -> Driver:
    async with async_session_factory() as session:
        query = select(Driver).where(Driver.id == driver_id)
        result = await session.execute(query)
        driver = result.mappings().one_or_none()
    if driver:
        return driver['Driver']


async def check_driver(id: int):
    async with async_session_factory() as session:
        query = select(func.count(Driver.id)).where(Driver.id == id)
        result = await session.execute(query)
        driver = result.scalar_one_or_none()
    if driver == 1:
        return True
    else:
        return False
