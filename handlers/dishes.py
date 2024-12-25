from aiogram import Router, F, types
from aiogram.filters import Command

from bot_config import database
from pprint import pprint

dishes_router = Router()

@dishes_router.message(Command("dishes"))
async def show_dishes(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Супы", callback_data="Супы"),
                types.InlineKeyboardButton(text="Горячие блюда", callback_data="Горячие блюда"),
                types.InlineKeyboardButton(text="Салаты", callback_data="Салаты"),
            ],
            [
                types.InlineKeyboardButton(text="Горячие напитки", callback_data="Горячие напитки"),
                types.InlineKeyboardButton(text="Холодные напитки", callback_data="Холодные напитки"),
                types.InlineKeyboardButton(text="Алкогольные напитки", callback_data="Алкогольные напитки"),
            ]

        ]
    )
    await message.answer("Выберите категорию, для отображения блюд:", reply_markup=kb)


@dishes_router.callback_query(F.data.in_(["Супы", "Горячие блюда", "Салаты", "Горячие напитки",
                                          "Холодные напитки", "Алкогольные напитки"]))
async def process_dishes(callback: types.CallbackQuery):
    selected_category = callback.data
    await callback.answer()
    dish_list = database.get_dishes_by_category()
    found_dish = False

    for dish in dish_list:
        if dish["category"] == selected_category:
            cover = dish["cover"]
            await callback.message.answer_photo(photo=cover,
                                               caption = f"Название: {dish['name']}\n"
                                                         f"Цена: {dish['price']}сом\n"
                                                         f"Категория : {dish['category']}\n")
            found_dish = True
    if not found_dish:
        await callback.message.answer(f"К сожалению, в категории '{selected_category}' нет блюд.")