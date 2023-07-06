import logging
from aiogram import executor
from bot import dp

# Configure logging
logging.basicConfig(level=logging.INFO)

from views import *

from db import migrate

# migrate()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
