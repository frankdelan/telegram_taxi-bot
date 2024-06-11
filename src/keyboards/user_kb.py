from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

btn_who_order = [
    [KeyboardButton(text='Мой профиль')],
    [KeyboardButton(text='Сделать заказ')]
]

btn_wh_order = [
    [KeyboardButton(text='Мой профиль')],
    [KeyboardButton(text='Отменить заказ')]
]

btn_wh_order_commit = [
    [KeyboardButton(text='Мой профиль')],
    [KeyboardButton(text='Отменить заказ')],
    [KeyboardButton(text='Подтвердить заказ')]
]

btn_register = [
    [KeyboardButton(text='Регистрация')]
]

share_location_button = [
    [KeyboardButton(text="Поделиться местоположением", request_location=True)]
]

share_number_button = [
    [KeyboardButton(text="Поделиться номером", request_contact=True)]
]


# Авторизованный пользователь без заказа
#   [Мой профиль] [Сделать заказ]
kb_make_order_user = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn_who_order)


# Авторизованный пользователь с заказом
#   [Мой профиль] [Отменить заказ]
kb_cancel_order_user = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn_wh_order)


# Авторизованный пользователь с заказом
#   [Мой профиль] [Отменить заказ]
#        [Подтвердить заказ]
kb_confirm_order_user = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn_wh_order_commit)


# Неавторизованный пользователь
#   [Регистрация]
kb_unauthorized_user = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn_register)


# Кнопка "взять заказ" в группе
#   [Взять заказ] -> def.callback(take)
inline_keyboard = InlineKeyboardBuilder()
inline_keyboard.add(InlineKeyboardButton(text='Взять заказ', callback_data='take'))

# Кнопка выбора типа автомобиля
car_type_keyboard = InlineKeyboardBuilder()
car_type_keyboard.add(InlineKeyboardButton(text='Механика', callback_data='0')). \
                  add(InlineKeyboardButton(text='Автомат', callback_data='1'))


# Кнопка "поделиться номером"
share_number_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                  one_time_keyboard=True,
                                                  keyboard=share_number_button)


# Кнопка "поделиться местоположением"
share_location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                    one_time_keyboard=True,
                                                    keyboard=share_location_button)

