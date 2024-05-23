from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from settings.db_config import token

bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
