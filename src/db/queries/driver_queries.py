from database import make_query, make_crud_query


@make_crud_query
async def add_driver(id, name, driver_data):
    return "INSERT INTO drivers(`id`, `name`, `number`, `car_model`,`car_color`,`car_number`) " \
           f"VALUES ({id}, '{name}','{driver_data.get('number')}','{driver_data.get('car_model')}'," \
           f"'{driver_data.get('car_color')}','{driver_data.get('car_number')}')"


@make_query
async def get_query_for_driver_data(driver_id):
    return f"SELECT `name`, `number`, `car_model`, `car_color`, `car_number` " \
          f"FROM drivers WHERE id = {driver_id}"


async def get_driver_data(driver_id):
    data = await get_query_for_driver_data(driver_id)
    if data:
        result = data[0]['name'], data[0]['number'], data[0]['car_model'], data[0]['car_color'], data[0]['car_number']
        return result


@make_query
async def get_query_for_driver_count(id):
    return f"SELECT COUNT(*) as count " \
          f"FROM drivers " \
          f"WHERE id = {id}"


async def check_driver(id):
    result = await get_query_for_driver_count(id)
    if result:
        if result[0]['count'] == 1:
            return True
        else:
            return False
