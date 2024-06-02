import logging 
import asyncio
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import BOT_TOKEN, LANGUAGES 
from db import DB 
from handlers import registration, matching, profile, support  


dp = Dispatcher()  
db_postgres = DB()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

# async def on_startup(dispatcher):     
#     dp.pool = DB()   
#     logging.info("Database connected and tables created")  
#     i18n = I18nMiddleware('bot', path='locales', default='en') 
#     dp.middleware.setup(i18n)  
#     registration.register_handlers(dp) 
#     matching.register_handlers(dp) 
#     profile.register_handlers(dp) 
#     support.register_handlers(dp)  


async def main():
    if BOT_TOKEN is None:
        return
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool = await db_postgres.get_pool()
    await dp.start_polling(bot)

if __name__ == "__main__":     
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())