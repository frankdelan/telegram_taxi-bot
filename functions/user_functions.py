from .database import make_query, make_crud_query


@make_crud_query
async def add_user(id, number):
    return f"INSERT INTO users(id, number) " \
        f"VALUES ({id}, {number})"


@make_query
async def get_query_for_phone_number(id_user):
    return f"SELECT number " \
        f"FROM users " \
        f"WHERE id = {id_user}"


async def get_phone(id_user):
    result = await get_query_for_phone_number(id_user)
    if result:
        return result[0]['number']


@make_query
async def get_query_for_user_count(id_user):
    return f"SELECT COUNT(*) as count " \
        f"FROM users " \
        f"WHERE id = {id_user}"


async def check_user(id_user):
    result = await get_query_for_user_count(id_user)
    if result:
        if result[0]['count'] == 1:
            return True
        else:
            return False
