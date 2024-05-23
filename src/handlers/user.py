from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message

from settings.bot_config import bot
from keyboards import kb_cancel_order_user, kb_unauthorized_user, kb_make_order_user, inline_keyboard, share_keyboard
from db.queries import (check_user, add_user, get_phone, check_order, get_last_order_id, get_id_order_message,
                        insert_id_order_message, make_order, cancel_order, confirm_order, get_last_user_order_id)

from settings.db_config import chat_id


user_router = Router()


class Registration(StatesGroup):
    registration_number = State()


class MakeOrder(StatesGroup):
    address_from = State()
    address_to = State()


@user_router.message(Command('start', 'help'))
async def start_handler(message: Message):
    await message.answer('Добро пожаловать в такси "Дельта" 🚕 ')

    if await check_user(message.from_user.id):
        if await check_order(message.from_user.id):
            await message.answer('⚠ У вас уже взят заказ', reply_markup=kb_cancel_order_user)
        else:
            await message.answer('Вы можете сделать заказ', reply_markup=kb_make_order_user)
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


@user_router.message(F.text == 'Регистрация')
async def registration_handler(message: Message, state: FSMContext):
    if message.text == "Регистрация" and not await check_user(message.from_user.id):
        await message.answer("Предоставьте свой номер для регистрации",
                             reply_markup=share_keyboard)
        await state.set_state(Registration.registration_number)
    elif message.text == "Регистрация" and await check_user(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!")


@user_router.message(F.text == 'Мой профиль')
async def profile_handler(message: Message):
    if await check_user(message.from_user.id):
        my_number = await get_phone(message.from_user.id)
        await message.answer(f"<b>Ваши данные</b>\n"
                             f"Имя : <b>{message.from_user.first_name}</b>\n"
                             f"Номер телефона : <b>{my_number}</b>",
                             parse_mode='html')
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


@user_router.message(F.text == 'Сделать заказ')
async def make_order_handler(message: Message, state: FSMContext):
    if await check_user(message.from_user.id):
        if not await check_order(message.from_user.id):
            await message.answer("Введите адрес, где вы находитесь :")
            await state.set_state(MakeOrder.address_from)
        elif message.text == "Сделать заказ" and await check_order(message.from_user.id):
            await message.answer("У вас уже взят заказ")
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


@user_router.message(MakeOrder.address_from)
async def input_address_from(message: Message, state: FSMContext):
    await state.update_data(address_from=message.text)
    await message.answer("Введите адрес, куда вы поедете :")
    await state.set_state(MakeOrder.address_to)


@user_router.message(MakeOrder.address_to)
async def input_address_to(message: Message, state: FSMContext):
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
                                              parse_mode='html', reply_markup=inline_keyboard.as_markup())

    await state.clear()
    await insert_id_order_message(message.from_user.id, id_order_message.message_id)


@user_router.message(F.text == 'Отменить заказ')
async def cancel_order_handler(message: Message):
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


@user_router.message(F.text == 'Подтвердить заказ')
async def confirm_order_handler(message: Message):
    if await check_user(message.from_user.id):
        if await check_order(message.from_user.id):
            await confirm_order(message.from_user.id)
            await message.answer("Заказ был подтвержден!", reply_markup=kb_make_order_user)
        else:
            await message.answer('У вас нет активных заказов', reply_markup=kb_make_order_user)
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=kb_unauthorized_user)


@user_router.message(Registration.registration_number)
async def input_number_handler(message: Message, state: FSMContext):
    await state.clear()
    phone_number = message.contact.phone_number
    await add_user(message.from_user.id, phone_number)

    await message.answer("Вы успешно зарегистрировались!")
    await message.answer("Теперь вы можете сделать заказ", reply_markup=kb_make_order_user)


@user_router.message()
async def understand_message_handler(message: Message):
    if not await check_user(message.from_user.id):
        await message.answer("Вы не зарегистрированы", reply_markup=kb_unauthorized_user)
    else:
        if await check_order(message.from_user.id):
            await message.answer("Введите /start для начала работы бота", reply_markup=kb_cancel_order_user)
        else:
            await message.answer("Введите /start для начала работы бота", reply_markup=kb_make_order_user)



# # Ввод номера
# dp.register_message_handler(input_number_handler, state=Registration.registration_number,
#                             content_types=types.ContentType.CONTACT)
