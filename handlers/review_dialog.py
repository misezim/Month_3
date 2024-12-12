from aiogram import Router, F, types
from aiogram. filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


survey_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@survey_router.message(Command("review"))
async def start_survey(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(RestourantReview.name)

@survey_router.message(RestourantReview.name)
async def start_survey(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=message.text)

    await message.answer("Ваш номер телефона: ")
    await state.set_state(RestourantReview.phone_number)

@survey_router.message(RestourantReview.phone_number)
async def start_survey(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.isdigit():
        await message.answer("Пожалуйста, введите только цифры для номера телефона.")
        return
    await state.update_data(phone_number=phone_number)
    await message.answer("Как оцениваете качество еды?", reply_markup=rating_keyboard())
    await state.set_state(RestourantReview.food_rating)

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


@survey_router.callback_query(RestourantReview.food_rating)
async def handle_food_rating(callback: types.CallbackQuery, state: FSMContext):
        food_rating = callback.data
        await state.update_data(food_rating=food_rating)

        await callback.message.answer("Как оцениваете чистоту заведения?", reply_markup=rating_keyboard())
        await state.set_state(RestourantReview.cleanliness_rating)
        await callback.answer()

@survey_router.callback_query(RestourantReview.cleanliness_rating)
async def handle_cleanliness_rating(callback: types.CallbackQuery, state: FSMContext):
        cleanliness_rating = callback.data
        await state.update_data(cleanliness_rating=cleanliness_rating)
        await callback.message.answer("Есть ли у вас дополнительные комментарии или жалобы?")
        await state.set_state(RestourantReview.extra_comments)
        await callback.answer()

@survey_router.message(RestourantReview.extra_comments)
async def get_extra_comments(message: types.Message, state: FSMContext):
    extra_comments = message.text
    await state.update_data(extra_comments=extra_comments)
    data = await state.get_data()
    await message.answer("Спасибо за ваш отзыв!")
    print(data)
    await state.clear()