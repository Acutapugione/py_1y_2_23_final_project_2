from aiogram.types import InlineKeyboardButton as in_kb
from aiogram import Bot, Dispatcher
from db import session, Genre, Film, select
import json
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Initialize bot and dispatcher
bot = Bot(token=json.load(open("vendor/secrets.json")).get("API_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# is_echo = False