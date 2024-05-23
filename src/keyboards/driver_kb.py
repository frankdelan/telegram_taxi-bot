from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_register = [
    [KeyboardButton(text='Зарегистрироваться')]
]


# Неавторизованный водитель
#   [Регистрация]
kb_unauthorized_driver = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=button_register)