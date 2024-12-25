from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import default_state

start_router = Router()

@start_router.message(Command("start"), default_state)
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