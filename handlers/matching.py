from db import DB
from aiogram.types import Message
from support.keyboards import get_matching_keyboard

async def get_matching(message: Message, db_postgres: DB, language:str) -> None:
    matching = await db_postgres.get_matching_customers(message.chat.id)
    if matching is not None:
        keyboard = get_matching_keyboard(language)
        await message.answer(matching, reply_markup=keyboard) # TODO доделать вывод анкеты
    else:
        await message.answer("No matching")