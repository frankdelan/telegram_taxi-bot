from aiogram.utils import executor
from create_bot import dp

from handlers import user, group, driver

driver.register_handlers_driver(dp)
user.register_handlers_user(dp)
group.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True)
