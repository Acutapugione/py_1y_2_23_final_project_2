from aiogram import types
from bot import dp, bot
import random
print(__name__)
is_echo = True



@dp.message_handler(commands=["start"])
async def welcome(message):
    print('START')
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🎲 Рандомне число", callback_data="random"),
            ],
            [
                types.InlineKeyboardButton("😊 Як справи?", callback_data="howdy"),
                types.InlineKeyboardButton("Ехо бот", callback_data="echo"),
            ],
            [types.InlineKeyboardButton("Фільми", callback_data="films")],
        ]
    )
    bot_data = await bot.get_me()
    text = f"""Привіт,{bot_data.first_name}!
    Я - <b>{message.from_user.first_name}</b>
    , бот створний для тесту."""
    await bot.send_message(
        message.chat.id, text, parse_mode="Markdown", reply_markup=markup
    )

@dp.callback_query_handler(lambda callb: callb.data == "random")
async def execute_random(callb: types.CallbackQuery):
    await callb.answer(str(random.randint(0, 100)))

@dp.callback_query_handler(lambda callb: callb.data == "howdy")
async def execute_howdy(callb: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                types.InlineKeyboardButton("Добре", callback_data="good"),
                types.InlineKeyboardButton("Не дуже", callback_data="bad"),
            ]
        ],
    )
    await callb.message.answer("Супер а сам як", reply_markup=markup)

@dp.callback_query_handler(lambda callb: callb.data == "echo")
async def execute_echo(callb: types.CallbackQuery):
    global is_echo
    is_echo = not is_echo
    await callb.answer("Echo " + "On" if is_echo else "Off")
    
    
@dp.message_handler(content_types=["text"])
async def lalala(message: types.Message):
    if is_echo:
        await message.answer(message.text)