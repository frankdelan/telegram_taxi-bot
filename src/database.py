import pymysql
from settings.db_config import host, user, password, db_name
from functools import wraps


async def get_connection() -> pymysql:
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )


def make_crud_query(func):
    @wraps(func)
    async def wrapper(*args):
        connection = await get_connection()
        cursor = connection.cursor()

        sql = await func(*args)

        cursor.execute(sql)
        connection.commit()
        connection.close()
    return wrapper


def make_query(func):
    @wraps(func)
    async def wrapper(*args):
        connection = await get_connection()
        cursor = connection.cursor()

        sql = await func(*args)

        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return result
    return wrapper
