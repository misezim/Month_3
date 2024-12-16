import asyncio
import logging

from bot_config import bot, dp, database
from handlers.start import start_router
from handlers.other_messages import other_router
from handlers.review_dialog import survey_router
async def on_startup(bot):
    database.create_tables()

async def main():
    dp.include_router(start_router)
    dp.include_router(other_router)
    dp.include_router(survey_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())