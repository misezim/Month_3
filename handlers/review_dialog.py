from aiogram import Router, F, types
from aiogram. filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot_config import database

survey_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@survey_router.message(Command("stop"))
@survey_router.message(F.text == "стоп")
async def stop_dialog(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос остановлен")


@survey_router.callback_query(F.data == "review")
async def start_survey(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Для остановки введите слово 'стоп'")
    await callback_query.message.answer("Как вас зовут?")
    await state.set_state(RestaurantReview.name)
    await callback_query.answer()


@survey_router.message(RestaurantReview.name)
async def start_survey(message: types.Message, state: FSMContext):
    name = message.text
    if len(name) < 3:
        await message.answer("Имя должно содержать хотя бы 3 символа.")
        return
    elif len(name) > 50:
        await message.answer("Имя не должно превышать 50 символов.")
        return
    await state.update_data(name=message.text)

    await message.answer("Ваш номер телефона: ")
    await state.set_state(RestaurantReview.phone_number)

@survey_router.message(RestaurantReview.phone_number)
async def start_survey(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.isdigit():
        await message.answer("Пожалуйста, введите только цифры для номера телефона.")
        return
    await state.update_data(phone_number=phone_number)
    await message.answer("Как оцениваете качество еды?", reply_markup=rating_keyboard())
    await state.set_state(RestaurantReview.food_rating)

def rating_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="1", callback_data="1"),
                types.InlineKeyboardButton(text="2", callback_data="2"),
                types.InlineKeyboardButton(text="3", callback_data="3"),
                types.InlineKeyboardButton(text="4", callback_data="4"),
                types.InlineKeyboardButton(text="5", callback_data="5"),
            ]
        ]
    )


@survey_router.callback_query(RestaurantReview.food_rating)
async def handle_food_rating(callback: types.CallbackQuery, state: FSMContext):
        food_rating = callback.data
        await state.update_data(food_rating=food_rating)

        await callback.message.answer("Как оцениваете чистоту заведения?", reply_markup=rating_keyboard())
        await state.set_state(RestaurantReview.cleanliness_rating)
        await callback.answer()

@survey_router.callback_query(RestaurantReview.cleanliness_rating)
async def handle_cleanliness_rating(callback: types.CallbackQuery, state: FSMContext):
        cleanliness_rating = callback.data
        await state.update_data(cleanliness_rating=cleanliness_rating)
        await callback.message.answer("Есть ли у вас дополнительные комментарии или жалобы?")
        await state.set_state(RestaurantReview.extra_comments)
        await callback.answer()

@survey_router.message(RestaurantReview.extra_comments)
async def get_extra_comments(message: types.Message, state: FSMContext):
    extra_comments = message.text
    await state.update_data(extra_comments=extra_comments)
    await message.answer("Спасибо за ваш отзыв!")
    data = await state.get_data()
    print(data)
    database.save_reviews(data)
    await state.clear()