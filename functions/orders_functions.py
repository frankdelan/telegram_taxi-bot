from .database import make_query, make_crud_query
from datetime import datetime


@make_crud_query
async def make_order(id_user, address_info):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"INSERT INTO orders(`id_user`, `address_from`,`address_to`, `date`, `status`) " \
           f"VALUES({id_user}, '{address_info[0]}','{address_info[1]}', '{now}', 'active')"


@make_query
async def get_query_for_order_count(id_user):
    return f"SELECT COUNT(*) as count " \
          f"FROM orders " \
          f"WHERE id_user = {id_user} AND status not in ('inactive', 'cancel')"


async def check_order(id_user):
    result = await get_query_for_order_count(id_user)
    if result:
        if result[0]['count'] == 1:
            return True
        else:
            return False


@make_crud_query
async def insert_id_order_message(id_user, id_order_message):
    return f"UPDATE orders SET id_order_message = {id_order_message} " \
           f"WHERE id_user = {id_user} AND status = 'active'"


@make_crud_query
async def cancel_order(id_user):
    return f"UPDATE orders " \
          f"SET status = 'cancel' WHERE id_user = {id_user} " \
          f"AND id = " \
          f"(SELECT MAX(id) AS max" \
          f"    FROM orders" \
          f"    WHERE id_user = {id_user} AND status <> 'inactive') "



@make_crud_query
async def confirm_order(id_user):
    return f"UPDATE orders " \
          f"SET status = 'inactive' WHERE id_user = {id_user} " \
          f"AND id = " \
          f"(SELECT MAX(id) AS max" \
          f"    FROM orders" \
          f"    WHERE id_user = {id_user} AND status <> 'cancel') "


@make_query
async def get_query_for_id_order_message(id_user):
    return f"SELECT id_order_message " \
           f"FROM orders WHERE id_user = {id_user} " \
           f"AND status = 'active'"


async def get_id_order_message(id_user):
    result = await get_query_for_id_order_message(id_user)
    if result:
        return result[0]['id_order_message']


@make_query
async def get_query_for_data_user_by_id(id_user):
    return f"SELECT address_from, address_to, users.number as number " \
          f"FROM orders INNER JOIN users " \
          f"ON orders.id_user = users.id " \
          f"WHERE orders.id_user = {id_user} AND orders.status = 'active'"


async def get_data_user_by_id(id_user):
    data = await get_query_for_data_user_by_id(id_user)
    if data:
        result = [data[0]['address_from'], data[0]['address_from'], data[0]['number']]
        return result


@make_query
async def get_query_for_last_order_id():
    return f"SELECT MAX(id) " \
          f"FROM orders"


async def get_last_order_id():
    data = await get_query_for_last_order_id()
    if data:
        return data[0]['MAX(id)']


@make_query
async def get_query_for_last_order_id_by_user(id_user):
    return f"SELECT MAX(id) " \
           f"FROM orders " \
           f"WHERE id_user = {id_user}"


async def get_last_user_order_id(id_user):
    data = await get_query_for_last_order_id_by_user(id_user)
    if data:
        return data[0]['MAX(id)']


@make_query
async def get_query_for_data_by_message_id(id_order_message):
    return f"SELECT orders.id_order_message, orders.address_from, orders.address_to, " \
          f"orders.id_user, users.number as number " \
          f"FROM orders INNER JOIN users ON orders.id_user = users.id " \
          f"WHERE id_order_message = {id_order_message}"


async def get_data_user_by_id_order_message(id_order_message):
    data = await get_query_for_data_by_message_id(id_order_message)
    if data:
        result = data[0]['id_order_message'], data[0]['address_from'], data[0]['address_to'], data[0]['number'], \
                 data[0]['id_user']
        return result
