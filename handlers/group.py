from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext

from functions import get_data_user_by_id_order_message, get_driver_data, check_driver, \
    get_last_user_order_id
from keyboards import kb_confirm_order_user

from config import chat_id


# @dp.callback_query_handler(lambda call: call.data == 'take', ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def taking_an_order(query: types.CallbackQuery, state: FSMContext):
    if await check_driver(query.from_user.id):
        id_order_message = query.message.message_id
        data = await get_data_user_by_id_order_message(id_order_message)
        order_id = await get_last_user_order_id(data[4])
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=
        f"✅ <b>Заказ № {order_id} взят</b> ✅\n"
        f"Местонахождение : <b>{data[1]}</b>\n"
        f"Конечный адрес : <b>{data[2]}</b>\n"
        f"Телефон клиента : <b>{data[3]}</b>\n"
        f"Заказ принял @{query.from_user.username}", parse_mode='html', reply_markup=None)

        info = await get_driver_data(query.from_user.id)
        await bot.send_message(data[4],
                               "✅ Ваш заказ был принят, ожидайте!\n"
                               f"Водитель : <b>{info[0]}</b>\n"
                               f"Номер водителя : <b>{info[1]}</b>\n"
                               f"Автомобиль : <b>{info[2]}</b>\n"
                               f"Цвет автомобиля : <b>{info[3]}</b>\n"
                               f"Номер автомобиля : <b>{info[4]}</b>\n\n"
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


def register_handlers_other(dp: Dispatcher):
    dp.register_callback_query_handler(taking_an_order, lambda call: call.data == 'take')
