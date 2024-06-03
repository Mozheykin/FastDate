import logging 
import asyncio
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from config import BOT_TOKEN, LANGUAGES, DEFAULT_CUSTOMER, START_MESSAGE
from language import ACTIVATE_MESSAGE, DEACTIVATE_MESSAGE, PROBLEM_LANGUAGE
from models.customer import Customer, CustomerView
from db import DB 
from handlers import registration, matching, profile, support  


dp = Dispatcher()  
logo_mp4 = FSInputFile('media/logo.MP4')
bot = None
db_postgres = DB()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    default_customer = Customer(**DEFAULT_CUSTOMER)
    default_customer.user_id = message.chat.id
    default_customer.username = message.from_user.full_name
    geted_customer = await db_postgres.get_customer(default_customer.user_id)
    if  geted_customer is None:
        language = default_customer.language
        await db_postgres.add_customer(default_customer)
        start_message = START_MESSAGE.get(language, PROBLEM_LANGUAGE)
        await message.answer_video(logo_mp4)
        await message.answer(start_message)
    else:
        default_customer = CustomerView(**geted_customer)
        language = default_customer.language
        if default_customer.is_active is not True:
            activate_message = DEACTIVATE_MESSAGE.get(language, PROBLEM_LANGUAGE)
            await db_postgres.activate_customer(default_customer.user_id)
            await message.answer(activate_message)
        else:
            activate_message = DEACTIVATE_MESSAGE.get(language, PROBLEM_LANGUAGE)
            await message.answer(activate_message)
            


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
    global bot
    if BOT_TOKEN is None:
        return
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool = await db_postgres.get_pool()
    await dp.start_polling(bot)

if __name__ == "__main__":     
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())