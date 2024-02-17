from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_register = KeyboardButton('Зарегистрироваться')

# Неавторизованный водитель
#   [Регистрация]
kb_unauthorized_driver = ReplyKeyboardMarkup(resize_keyboard=True)
kb_unauthorized_driver.add(button_register)
