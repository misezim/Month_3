from aiogram import Router, types, F
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "Оствить отзыв", callback_data="review"),
            ],

        ]
    )
    await message.answer(f"Добро пожаловать! {name}, Если вы хотите оставить отзыв, нажмите кнопку ниже:", reply_markup=kb)

@start_router.callback_query(F.data == "review")
async def review(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Введите /review на командной строке")