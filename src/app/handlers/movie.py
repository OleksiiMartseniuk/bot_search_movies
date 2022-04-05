import time
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hbold

from src.database.db import session
from src.database.models import Group, Movie
from src.services.utils import MovieServices

from datetime import datetime


# Category
with session as s:
    available_category_names = []
    category_names_query = s.query(Group.title)
    for item in category_names_query:
        available_category_names.append(item[0])

# Menu
available_menu_names = ['Вывод всех фильмов', 'Топ 10 фильмов', 'Рандомный фильм']


def card(item: Movie) -> tuple:
    cart = f'{hbold("Title: ")}{item.title}\n' \
           f'{hbold("Full Title: ")}{item.full_title}\n' \
           f'{hbold("Year: ")}{item.year}\n' \
           f'{hbold("Crew: ")}{item.crew}\n' \
           f'{hbold("ImDbRating: ")}{item.imDbRating}\n' \
           f'{hbold("ImDbRatingCount: ")}{item.imDbRatingCount}\n' \
           f'{hbold("Rank: ")}{item.rank}'
    image = item.image
    return (image, cart)


def list_card(item: Movie) -> tuple:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Подробние..", callback_data=f"movie_{item.id}"))
    content = f'{item.rank}: {item.title}'
    return (content, keyboard)


class OrderMovie(StatesGroup):
    waiting_for_category_names = State()
    waiting_for_menu_names = State()


async def movie_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for title in available_category_names:
        keyboard.add(title)
    await message.answer('Выберите категорию:', reply_markup=keyboard)
    await OrderMovie.waiting_for_category_names.set()


async def movie_category(message: types.Message, state: FSMContext):
    if message.text not in available_category_names:
        await message.answer("Пожалуйста, выберите категорию, используя клавиатуру ниже.")
        return
    await state.update_data(movie_category=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for title in available_menu_names:
        keyboard.add(title)

    await OrderMovie.next()
    await message.answer("Теперь выберите действия:", reply_markup=keyboard)


async def movie_menu(message: types.Message, state: FSMContext):
    if message.text not in available_menu_names:
        await message.answer("Пожалуйста, выберите действия, используя клавиатуру ниже.")
        return

    user_data = await state.get_data()
    client_movie = MovieServices(user_data.get('movie_category'))
    if message.text == 'Вывод всех фильмов':
        logging.info(f'User: {message.from_user.id} -> movie_all -- {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')

        data = client_movie.movie_all()
        await message.answer('Збор Данных...', reply_markup=types.ReplyKeyboardRemove())
        for index, item in enumerate(data):
            content, keyboard = list_card(item)
            await message.answer(content, reply_markup=keyboard)
            if index % 20 == 0:
                time.sleep(3)
        await message.answer('Збор завершон')

    if message.text == 'Топ 10 фильмов':
        logging.info(f'User: {message.from_user.id} -> movie_top -- {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')

        data = client_movie.movie_top(10)
        await message.answer('Збор Данных...', reply_markup=types.ReplyKeyboardRemove())
        for index, item in enumerate(data):
            content, keyboard = list_card(item)
            await message.answer(content, reply_markup=keyboard)

    if message.text == 'Рандомный фильм':
        logging.info(f'User: {message.from_user.id} -> movie_rang -- {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')

        item = client_movie.movie_rang()
        image, content = card(item)
        await message.answer_photo(image, caption=content, reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


async def movie_id_card(call: types.CallbackQuery):
    logging.info(f'User: {call.from_user.id} -> movie_id -- {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')

    movie_id = call.data.split("_")[1]
    movie = MovieServices.movie_id(movie_id)
    image, content = card(movie)
    await call.message.answer_photo(image, caption=content, reply_markup=types.ReplyKeyboardRemove())


def register_handlers_movie(dp: Dispatcher):
    dp.register_message_handler(movie_start, commands="movie", state="*")
    dp.register_message_handler(movie_category, state=OrderMovie.waiting_for_category_names)
    dp.register_message_handler(movie_menu, state=OrderMovie.waiting_for_menu_names)
    dp.register_callback_query_handler(movie_id_card, Text(startswith="movie_"))
