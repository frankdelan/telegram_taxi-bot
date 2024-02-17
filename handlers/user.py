from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from keyboards import kb_cancel_order_user, kb_unauthorized_user, kb_make_order_user, inline_keyboard, share_keyboard
from functions import check_user, check_order, add_user, get_last_order_id , \
    get_phone, get_id_order_message, insert_id_order_message, make_order, cancel_order, confirm_order, \
    get_last_user_order_id

from config import chat_id


class Registration(StatesGroup):
    registration_number = State()


class MakeOrder(StatesGroup):
    address_from = State()
    address_to = State()


# @dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.message):
    await message.answer('Добро пожаловать в такси "Дельта"  🚕 ')

    if await check_user(message.from_user.id):
        if await check_order(message.from_user.id):
            await message.answer('⚠ У вас уже взят заказ', reply_markup=kb_cancel_order_user)
        else:
            await message.answer('Вы можете сделать заказ', reply_markup=kb_make_order_user)
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='Регистрация')
async def registration_handler(message: types.message):
    if message.text == "Регистрация" and not await check_user(message.from_user.id):
        await message.answer("Предоставьте свой номер для регистрации",
                             reply_markup=share_keyboard)

        await Registration.registration_number.set()
    elif message.text == "Регистрация" and await check_user(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!")


# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='Мой профиль')
async def profile_handler(message: types.message):
    if await check_user(message.from_user.id):
        my_number = await get_phone(message.from_user.id)
        await message.answer(f"<b>Ваши данные</b>\n"
                             f"Имя : <b>{message.from_user.first_name}</b>\n"
                             f"Номер телефона : <b>{my_number}</b>",
                             parse_mode='html')
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='Сделать заказ')
async def make_order_handler(message: types.message):
    if await check_user(message.from_user.id):
        if not await check_order(message.from_user.id):
            await message.answer("Введите адрес, где вы находитесь :")
            await MakeOrder.address_from.set()
        elif message.text == "Сделать заказ" and await check_order(message.from_user.id):
            await message.answer("У вас уже взят заказ")
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


# @dp.message_handler(state=TakeOrder.address_from)
async def input_address_from(message: types.Message, state: FSMContext):
    await state.update_data(address_from=message.text)
    await message.answer("Введите адрес, куда вы поедете :")
    await MakeOrder.next()


# @dp.message_handler(state=TakeOrder.address_to)
async def input_address_to(message: types.Message, state: FSMContext):
    await state.update_data(address_to=message.text)
    user_data = await state.get_data()
    address_info = [user_data.get('address_from'), user_data.get('address_to')]
    await make_order(message.from_user.id, address_info)
    await message.answer("Ваш заказ передан в службу.\n"
                         "Мы оповестим вас, когда найдется водитель!\n"
                         "Это не займет много времени", reply_markup=kb_cancel_order_user)

    number = await get_phone(message.from_user.id)
    last_order_id = await get_last_order_id()
    id_order_message = await bot.send_message(chat_id,
                                              f"❗️ <b>Получен заказ № {last_order_id}</b> ❗️\n"
                                              f"Местонахождение : <b>{user_data['address_from']}</b>\n"
                                              f"Конечный адрес : <b>{user_data['address_to']}</b>\n"
                                              f"Телефон клиента : <b>{number}</b>",
                                              parse_mode='html', reply_markup=inline_keyboard)

    await state.finish()
    await insert_id_order_message(message.from_user.id, id_order_message.message_id)


# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='Отменить заказ')
async def cancel_order_handler(message: types.message):
    if await check_user(message.from_user.id):
        if await check_order(message.from_user.id):
            message_id = await get_id_order_message(message.from_user.id)
            order_id = await get_last_user_order_id(message.from_user.id)

            await cancel_order(message.from_user.id)

            await message.answer("Ваш заказ отменен", reply_markup=kb_make_order_user)
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=
                                        f"<b>⚠ Внимание! ⚠</b>\n"
                                        f"Заказ <b>№{order_id}</b> был отменён!",
                                        parse_mode='html')
        else:
            await message.answer('У вас нет активных заказов', reply_markup=kb_make_order_user)
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='Подтвердить заказ')
async def confirm_order_handler(message: types.message):
    if await check_user(message.from_user.id):
        if await check_order(message.from_user.id):
            await confirm_order(message.from_user.id)
            await message.answer("Заказ был подтвержден!", reply_markup=kb_make_order_user)
        else:
            await message.answer('У вас нет активных заказов', reply_markup=kb_make_order_user)
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


# @dp.message_handler(state=Registration.registration_number)
async def input_number_handler(message: types.Message, state: FSMContext):
    await state.finish()
    phone_number = message.contact.phone_number
    await add_user(message.from_user.id, phone_number)

    await message.answer("Вы успешно зарегистрировались!")
    await message.answer("Теперь вы можете сделать заказ", reply_markup=kb_make_order_user)


# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def understand_message_handler(message: types.message):
    if not await check_user(message.from_user.id):
        await message.answer("Вы не зарегистрированы", reply_markup=kb_unauthorized_user)
    else:
        if await check_order(message.from_user.id):
            await message.answer("Введите /start для начала работы бота", reply_markup=kb_cancel_order_user)
        else:
            await message.answer("Введите /start для начала работы бота", reply_markup=kb_make_order_user)


def register_handlers_user(dp: Dispatcher):
    # ['/start', '/help']
    dp.register_message_handler(start_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                commands=['start', 'help'])
    # ['Регистрация']
    dp.register_message_handler(registration_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                text='Регистрация')
    # Ввод номера
    dp.register_message_handler(input_number_handler, state=Registration.registration_number,
                                content_types=types.ContentType.CONTACT)

    # ['Мой профиль']
    dp.register_message_handler(profile_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='Мой профиль')

    # ['Сделать заказ']
    dp.register_message_handler(make_order_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                text='Сделать заказ')

    # ['Отменить заказ']
    dp.register_message_handler(cancel_order_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                text='Отменить заказ')

    # ['Подтвердить заказ']
    dp.register_message_handler(confirm_order_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                text='Подтвердить заказ')
    # Ввод адреса от и до
    dp.register_message_handler(input_address_from, state=MakeOrder.address_from)
    dp.register_message_handler(input_address_to, state=MakeOrder.address_to)

    # Нераспознанное сообщение
    dp.register_message_handler(understand_message_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
