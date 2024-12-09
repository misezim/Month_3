import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values

token = dotenv_values(".env").get("BOT_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()

random_names = ("Alice", "Bob", "Charlie", "Diana", "Frank",
                "Grace", "Hannah", "Igor", "Jack")

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"HI! {name}")

@dp.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    name = message.from_user.first_name
    id = message.from_user.id
    last_name = message.from_user.last_name if message.from_user.last_name else "No last name"
    await message.answer(f" Your name = {name},\nYour id = {id},\nYour last name = {last_name}")

@dp.message(Command("random"))
async def random_handler(message: types.Message):
    random_name = random.choice(random_names)
    await message.answer(f"Random name: {random_name}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())