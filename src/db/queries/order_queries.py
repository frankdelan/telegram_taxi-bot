from datetime import datetime
from sqlalchemy import select, func, update
from sqlalchemy.exc import IntegrityError

from database import async_session_factory
from db.models import Order, User, Status


async def make_order(id_user: int, address_info: tuple):
    order = Order(id_user=id_user, address_from=address_info[0],
                  address_to=address_info[1], date=datetime.now(), status=Status.ACTIVE)
    async with async_session_factory() as session:
        session.add(order)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def check_order(id_user: int) -> bool:
    async with async_session_factory() as session:
        query = select(func.count(Order.id)).where((Order.id_user == id_user) &
                                                   (Order.status.not_in([Status.INACTIVE, Status.CANCEL])))
        result = await session.execute(query)
        order = result.scalar_one_or_none()
    if order == 1:
        return True
    else:
        return False


async def insert_id_order_message(id_user: int, id_order_message: int):
    async with async_session_factory() as session:
        stmt = update(Order).where((Order.id_user == id_user) &
                                   (Order.status == Status.ACTIVE)).values(id_order_message=id_order_message)
        await session.execute(stmt)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def cancel_order(id_user):
    async with async_session_factory() as session:
        subquery = select(func.max(Order.id)).where(
            (Order.id_user == id_user) & (Order.status != Status.INACTIVE)).scalar_subquery()

        stmt = update(Order).where((Order.id_user == id_user) &
                                   (Order.id == subquery)).values(status=Status.CANCEL)
        await session.execute(stmt)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def confirm_order(id_user):
    async with async_session_factory() as session:
        subquery = select(func.max(Order.id)).where(
            (Order.id_user == id_user) & (Order.status == Status.CANCEL)).scalar_subquery()

        stmt = update(Order).where((Order.id_user == id_user) &
                                   (Order.id == subquery)).values(status=Status.INACTIVE)
        await session.execute(stmt)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def get_id_order_message(id_user: int):
    async with async_session_factory() as session:
        query = select(Order.id_order_message).where((Order.id_user == id_user) & (Order.status == Status.ACTIVE))
        result = await session.execute(query)
        order_id = result.scalar_one_or_none()
    if order_id:
        return order_id


async def get_data_user_by_id(id_user: int):
    async with async_session_factory() as session:
        query = select(Order.address_from, Order.address_to, User.number
                       ).join(User, Order.id_user == User.id
                              ).where((Order.id_user == id_user) & (Order.status == Status.ACTIVE))
        result = await session.execute(query)
        order_info = result.mappings().one_or_none()
    if order_info:
        return order_info


async def get_last_order_id():
    async with async_session_factory() as session:
        query = select(func.max(Order.id))
        result = await session.execute(query)
        order_id = result.scalar_one_or_none()
    if order_id:
        return order_id


async def get_last_user_order_id(id_user: int):
    async with async_session_factory() as session:
        query = select(func.max(Order.id)).where(Order.id_user == id_user)
        result = await session.execute(query)
        order_id = result.scalar_one_or_none()
    if order_id:
        return order_id


async def get_data_user_by_id_order_message(id_order_message: int):
    async with async_session_factory() as session:
        query = select(Order.id_order_message, Order.address_from, Order.address_to, Order.id_user, User.number
                       ).join(User, Order.id_user == User.id
                              ).where(Order.id_order_message == id_order_message)
        result = await session.execute(query)
        order_info = result.mappings().one_or_none()
    if order_info:
        return order_info
