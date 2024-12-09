import random
from aiogram import Router, types
from aiogram.filters import Command
other_router = Router()

menu = [
    {
    'name' : 'Pepperoni pizza',
    'recipe' : '1 pizza dough, 1/2 cup pizza sauce, 1/2 cups shredded mozzarella cheese, '
               '1/2 cup sliced pepperoni, 1 tablespoon olive oil, Dried oregano or basil',
    'image' : 'Pepperoni.jpg'},

    {
    'name' : 'Lasagna',
    'recipe' : '9 lasagna noodles (regular or no-boil), 1 lb ground beef or turkey, '
               '1 jar marinara sauce, 1 ½ cups ricotta cheese, 2 cups shredded mozzarella cheese, '
                '1 cup grated Parmesan cheese, 1 egg, 2 tbsp dried basil, Salt & pepper to taste',
    'image' : 'Lasagna.jpg'},

    {
    'name' : 'Carbonara',
    'recipe': '12 oz spaghetti (or pasta of choice), 4 oz pancetta or bacon, chopped, '
                  '2 large eggs, 1 cup grated Parmesan cheese, 2 cloves garlic, minced, '
                  'Salt & pepper to taste, Fresh parsley',
    'image' : 'Carbonara.jpg'
    }
]


# @other_router.message(Command("myinfo"))
# async def myinfo_handler(message: types.Message):
#     name = message.from_user.first_name
#     id = message.from_user.id
#     last_name = message.from_user.last_name if message.from_user.last_name else "No last name"
#     await message.answer(f" Your name = {name},\nYour id = {id},\nYour last name = {last_name}")

@other_router.message(Command("random"))
async def random_handler(message: types.Message):
    random_recipe = random.choice(menu)
    image_path = f"images/{random_recipe['image']}"
    image = types.FSInputFile(image_path)
    await message.answer_photo(image, caption=f"Name: {random_recipe['name']}\n"
                                              f"Recipe: {random_recipe['recipe']}")
