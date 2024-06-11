from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message

from db.queries import add_driver, check_admin
from utils import parse_driver_data

driver_router = Router()


class RegistrationDriver(StatesGroup):
    registration_driver = State()


@driver_router.message(Command("driver"))
async def start_handler(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer(f"Для регистрации нового водителя отправьте данные в таком формате")
        await message.answer("Фамилия:Иванов,\n"
                             "Имя:Иван,\n"
                             "Отчество:Иванович,\n"
                             "Номер телефона:XXXXXXXXXX,\n"
                             "Telegram:username")
        await state.set_state(RegistrationDriver.registration_driver)
    else:
        await message.answer(f"У вас нет прав администратора!")


@driver_router.message(RegistrationDriver.registration_driver)
async def registration_driver(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await state.update_data(driver_data=message.text)
        raw_data = await state.get_data()
        try:
            data: dict = await parse_driver_data(raw_data['driver_data'])
        except Exception as e:
            await message.answer(f"Некорректные данные!\n{e}")
            await state.clear()
            return
        try:
            await add_driver(data)
            await message.answer(f"Водитель был успешно зарегистрирован!")
        except Exception as e:
            await message.answer(f"Водитель не был зарегистрирован!\n{e}")
            return
        finally:
            await state.clear()
    else:
        await message.answer(f"У вас нет прав администратора!")
