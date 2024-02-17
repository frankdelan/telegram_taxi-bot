from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from keyboards import kb_unauthorized_driver, share_keyboard, kb_make_order_user
from functions import add_driver, check_driver


class RegistrationDriver(StatesGroup):
    registration_number_driver = State()
    registration_car_model = State()
    registration_car_color = State()
    registration_car_number = State()


# @dp.message_handler(commands=['driver'])
async def start_handler(message: types.message):
    if await check_driver(message.from_user.id):
        await message.answer(f"Вы уже зарегистрированы!",
                             reply_markup=kb_make_order_user)
    else:
        await message.answer(f"Здравствуйте, {message.from_user.first_name}")
        await message.answer(f"Вам нужно пройти регистрацию!",
                             reply_markup=kb_unauthorized_driver)


# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='Зарегистрироваться')
async def registration_driver(message: types.message):
    if message.text == "Зарегистрироваться" and not await check_driver(message.from_user.id):
        await message.answer("Предоставьте свой номер для регистрации",
                             reply_markup=share_keyboard)
        await RegistrationDriver.registration_number_driver.set()
    elif message.text == "Зарегистрироваться" and await check_driver(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!")


# @dp.message_handler(state=RegistrationDriver.registration_number)
async def input_number_driver(message: types.Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await message.answer("Введите модель автомобиля\n"
                         "Пример : <b>Mitsubishi Lancer</b>",
                         reply_markup=None,
                         parse_mode='html')
    await RegistrationDriver.next()


# @dp.message_handler(state=RegistrationDriver.registration_car_model)
async def input_car_model(message: types.Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await message.answer("Введите цвет автомобиля")
    await RegistrationDriver.next()


# @dp.message_handler(state=RegistrationDriver.registration_car_model)
async def input_car_color(message: types.Message, state: FSMContext):
    await state.update_data(car_color=message.text)
    await message.answer("Введите номер автомобиля\n"
                         "Пример: <b>н065мк</b>",
                         parse_mode='html')
    await RegistrationDriver.next()


# @dp.message_handler(state=RegistrationDriver.registration_car_model)
async def input_car_number(message: types.Message, state: FSMContext):
    await state.update_data(car_number=message.text)

    driver_data = await state.get_data()

    await add_driver(message.from_user.id, message.from_user.first_name, driver_data)

    await state.finish()

    await message.answer("Вы были успешно зарегистрированы!")


def register_handlers_driver(dp: Dispatcher):
    # ['/driver']
    dp.register_message_handler(start_handler, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                commands=['driver'])

    # ['Регистрация']
    dp.register_message_handler(registration_driver, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                text='Зарегистрироваться')

    # Ввод номера телефона
    dp.register_message_handler(input_number_driver, state=RegistrationDriver.registration_number_driver,
                                content_types=types.ContentType.CONTACT)

    # Ввод модели автомобиля
    dp.register_message_handler(input_car_model, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                state=RegistrationDriver.registration_car_model)

    # Ввод цвета автомобиля
    dp.register_message_handler(input_car_color, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                state=RegistrationDriver.registration_car_color)

    # Ввод номера автомобиля
    dp.register_message_handler(input_car_number, ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                state=RegistrationDriver.registration_car_number)
