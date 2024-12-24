from aiogram import Router, F, types
from aiogram.filters import Command

from bot_config import database
from pprint import pprint

dishes_router = Router()
@dishes_router.message(Command("dishes"))
async def show_all_dishes(message: types.Message):
    dish_list = database.get_all_dishes()
    pprint(dish_list)
    for dish in dish_list:
        await message.answer(f"Название: {dish['name']}\n"
                             f"Цена: {dish['price']}\n"
                             f"Категория : {dish['category']}\n")
