from aiogram import Router, F, types
from aiogram. filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot_config import database

new_menu_router = Router()
new_menu_router.message.filter(F.from_user.id == 1105418521)
new_menu_router.callback_query.filter(F.from_user.id == 1105418521)

class NewDishes(StatesGroup):
    name = State()
    price = State()
    description = State()
    category= State()

@new_menu_router.message(Command("new_dish"))
async def create_new_dish(message: types.Message, state: FSMContext):
    await message.answer("Введите название нового блюда")
    await state.set_state(NewDishes.name)

@new_menu_router.message(NewDishes.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    print(name)
    await state.update_data(name=message.text)
    await message.answer("Введите цену блюда")
    await state.set_state(NewDishes.price)

@new_menu_router.message(NewDishes.price)
async def process_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("Пожалуйста, введите только цифры")
        return
    price = int(price)
    await state.update_data(price=price)
    await message.answer("Введите описание блюда?")
    await state.set_state(NewDishes.description)


@new_menu_router.message(NewDishes.description)
async def process_name(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    kb = types.ReplyKeyboardMarkup(
        keyboard=
        [
            [
                types.KeyboardButton(text="Супы"),
                types.KeyboardButton(text="Горячие блюда"),
                types.KeyboardButton(text="Салаты")
            ],
            [
                types.KeyboardButton(text="Горячие напитки"),
                types.KeyboardButton(text="Холодные напитки"),
                types.KeyboardButton(text="Алкогольные напитки"),
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите категорию: "
    )
    await message.answer("Выберите к какой категории относится это блюдо: ", reply_markup=kb)
    await state.set_state(NewDishes.category)

@new_menu_router.message(NewDishes.category)
async def process_genre(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.update_data(category=message.text)
    await message.answer("Блюдо сохранено!", reply_markup=kb)
    data = await state.get_data()
    print(data)
    database.save_dish(data)
    await state.clear()
