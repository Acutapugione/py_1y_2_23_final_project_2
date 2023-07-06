from aiogram import types
from bot import dp, bot
from models import Film, Genre
from db import session, select
from aiogram.types import InlineKeyboardMarkup as in_kb_m
from aiogram.types import InlineKeyboardButton as in_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FilmCreateForm(StatesGroup):
    name = State()
    author = State()
    genre = State()
    year = State()


# {
#     "name": "Бійцівський Клуб",
#     "author": "Чак Паланик",
#     "genre_id": 3,
#     "year": 1999
# }
@dp.message_handler(
    lambda message: message.text.isdigit(),
    state=FilmCreateForm.year,
)
async def process_year(message: types.Message, state: FSMContext):
    await state.update_data(year=int(message.text))
    async with state.proxy() as data:
        genre = session.get(Genre, data['genre'])
        p = Film(name=data['name'], author=data['author'], genre=genre, year=data['year'])
        session.add(p)
        session.commit()
        await message.answer(
            f"Good job {p}"
        )
        
    await state.finish()
    


@dp.callback_query_handler(
    lambda callb: str(callb.data).startswith("genre/"),
    state=FilmCreateForm.genre,
)
async def process_genre(callb: types.CallbackQuery, state: FSMContext):
    await FilmCreateForm.next()

    genre_id = int(callb.data.split("/")[-1])
    genre = session.get(Genre, genre_id)
    await state.update_data(genre=genre_id)

    await callb.message.reply(
        "Вкажіть рік.",
    )


@dp.message_handler(state=FilmCreateForm.author)
async def process_author(message: types.Message, state: FSMContext):
    # Робота з машиною станів
    await FilmCreateForm.next()
    await state.update_data(author=message.text)
    # Робота з клавіатурою
    request = select(Genre)
    genres = session.scalars(request)
    buttons = [
        types.InlineKeyboardButton(x.name, callback_data=f"genre/{x.id}")
        for x in genres
    ]
    markup = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[buttons[: len(buttons) // 2], buttons[len(buttons) // 2 :]],
    )
    await message.reply(
        "Вкажіть жанр.",
        reply_markup=markup,
    )


@dp.message_handler(state=FilmCreateForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await FilmCreateForm.next()
    await state.update_data(name=message.text)
    await message.reply("Вкажіть автора.")


@dp.callback_query_handler(lambda callb: callb.data == "create_film")
async def create_film(callb: types.CallbackQuery):
    await callb.answer("Вкажіть назву фільму.")
    await FilmCreateForm.name.set()


@dp.callback_query_handler(lambda callb: callb.data == "films")
async def get_films(callb: types.CallbackQuery):
    request = select(Film)
    films = session.scalars(request)
    buttons = [in_kb(x.name, callback_data=f"film/{x.id}") for x in films]
    buttons += [in_kb("Створити новий", callback_data="create_film")]
    markup = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[buttons[: len(buttons) // 2], buttons[len(buttons) // 2 :]],
    )
    for film in films:
        await callb.message.reply(film, parse_mode="Markdown")
    await callb.message.answer("Виберіть фільм", reply_markup=markup)


@dp.callback_query_handler(lambda callb: str(callb.data).startswith("film/"))
async def get_film_info(callb: types.CallbackQuery):
    film_id = int(callb.data.split("/")[-1])
    film = session.get(Film, film_id)

    await callb.message.reply(film, parse_mode="Markdown")
