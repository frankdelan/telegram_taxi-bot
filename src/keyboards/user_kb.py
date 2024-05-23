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

share_button = [
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


# Кнопка "поделиться номером"
share_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=share_button)
