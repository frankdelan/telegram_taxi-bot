from aiogram import Router, F, types

from db.models import Driver
from settings.bot_config import bot

from db.queries import get_data_user_by_id_order_message, get_last_user_order_id, get_driver_data, check_driver
from keyboards import kb_confirm_order_user

from settings.db_config import chat_id

group_router = Router()


@group_router.callback_query(F.data == 'take')
async def taking_an_order(query: types.CallbackQuery):
    if await check_driver(query.from_user.id):
        id_order_message = query.message.message_id
        data = await get_data_user_by_id_order_message(id_order_message)
        order_id = await get_last_user_order_id(data['id_user'])
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=
        f"✅ <b>Заказ № {order_id} взят</b> ✅\n"
        f"Местонахождение : <b>{data['address_from']}</b>\n"
        f"Конечный адрес : <b>{data['address_to']}</b>\n"
        f"Телефон клиента : <b>{data['number']}</b>\n"
        f"Заказ принял @{query.from_user.username}", parse_mode='html', reply_markup=None)

        driver: Driver = await get_driver_data(query.from_user.id)
        await bot.send_message(data['id_user'],
                               "✅ Ваш заказ был принят, ожидайте!\n"
                               f"Водитель : <b>{driver.name}</b>\n"
                               f"Номер водителя : <b>{driver.number}</b>\n"
                               f"Автомобиль : <b>{driver.car_model}</b>\n"
                               f"Цвет автомобиля : <b>{driver.car_color}</b>\n"
                               f"Номер автомобиля : <b>{driver.car_number}</b>\n\n"
                               f"❗ <b>Нажмите [Подтвердить заказ], когда водитель доставит вас до назначенного "
                               f"адреса</b>",
                               reply_markup=kb_confirm_order_user,
                               parse_mode='html')
    else:
        await bot.send_message(chat_id,
                               f"Водитель <b>[{query.from_user.first_name} - @{query.from_user.username}]</b> не "
                               f"зарегистрирован!\n "
                               f"Введите <b>/driver</b> в боте <b>taxiDelta_bot</b>, чтобы пройти регистрацию.\n"
                               f"После этого вы сможете принимать заказы.",
                               parse_mode='html')
