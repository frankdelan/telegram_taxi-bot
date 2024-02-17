from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

button_profile = KeyboardButton('Мой профиль')
button_take_order = KeyboardButton('Сделать заказ')
button_cancel_order = KeyboardButton('Отменить заказ')
button_register = KeyboardButton('Регистрация')
button_confirm_order = KeyboardButton('Подтвердить заказ')

# Авторизованный пользователь без заказа
#   [Мой профиль] [Сделать заказ]
kb_make_order_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_make_order_user.row(button_profile, button_take_order)

# Авторизованный пользователь с заказом
#   [Мой профиль] [Отменить заказ]
kb_cancel_order_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel_order_user.add(button_profile, button_cancel_order)

# Авторизованный пользователь с заказом
#   [Мой профиль] [Отменить заказ]
#        [Подтвердить заказ]
kb_confirm_order_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_confirm_order_user.add(button_profile, button_cancel_order)
kb_confirm_order_user.add(button_confirm_order)

# Неавторизованный пользователь
#   [Регистрация]
kb_unauthorized_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_unauthorized_user.add(button_register)

# Кнопка "взять заказ" в группе
#   [Взять заказ] -> def.callback(take)
inline_button = InlineKeyboardButton(text='Взять заказ', callback_data='take')
inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(inline_button)

# Кнопка "поделиться номером"
share_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
share_button = types.KeyboardButton(text="Поделиться номером", request_contact=True)
share_keyboard.add(share_button)
