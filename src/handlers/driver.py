from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import share_keyboard, kb_make_order_user, kb_unauthorized_driver
from db.queries import add_driver, check_driver

driver_router = Router()


class RegistrationDriver(StatesGroup):
    registration_number_driver = State()
    registration_car_model = State()
    registration_car_color = State()
    registration_car_number = State()


@driver_router.message(Command("driver"))
async def start_handler(message: Message):
    if await check_driver(message.from_user.id):
        await message.answer(f"Вы уже зарегистрированы!",
                             reply_markup=kb_make_order_user)
    else:
        await message.answer(f"Здравствуйте, {message.from_user.first_name}")
        await message.answer(f"Вам нужно пройти регистрацию!",
                             reply_markup=kb_unauthorized_driver)


@driver_router.message(F.text == 'Зарегистрироваться')
async def registration_driver(message: Message, state: FSMContext):
    if message.text == "Зарегистрироваться" and not await check_driver(message.from_user.id):
        await message.answer("Предоставьте свой номер для регистрации",
                             reply_markup=share_keyboard)
        await state.set_state(RegistrationDriver.registration_number_driver)
    elif message.text == "Зарегистрироваться" and await check_driver(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!")


@driver_router.message(RegistrationDriver.registration_number_driver)
async def input_number_driver(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await message.answer("Введите модель автомобиля\n"
                         "Пример : <b>Mitsubishi Lancer</b>",
                         reply_markup=None,
                         parse_mode='html')
    await state.set_state(RegistrationDriver.registration_car_model)


@driver_router.message(RegistrationDriver.registration_car_model)
async def input_car_model(message: Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await message.answer("Введите цвет автомобиля")
    await state.set_state(RegistrationDriver.registration_car_color)


@driver_router.message(RegistrationDriver.registration_car_color)
async def input_car_color(message: Message, state: FSMContext):
    await state.update_data(car_color=message.text)
    await message.answer("Введите номер автомобиля\n"
                         "Пример: <b>н065мк</b>",
                         parse_mode='html')
    await state.set_state(RegistrationDriver.registration_car_number)


@driver_router.message(RegistrationDriver.registration_car_number)
async def input_car_number(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)

    driver_data = await state.get_data()

    await add_driver(message.from_user.id, message.from_user.first_name, driver_data)

    await state.clear()

    await message.answer("Вы были успешно зарегистрированы!")
