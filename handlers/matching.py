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


async def matching(db_postgres: DB) -> None:
    customers = await db_postgres.get_customers()
    if customers is None:
        return
    for customer1 in customers:
        customer1_matching = await db_postgres.get_matching_customers(customer1.user_id)
        for customer2 in customers:
            if customer1.user_id == customer2.user_id:
                continue
            elif customer1_matching is not None and customer2.user_id not in customer1_matching:
                customer1_matching.append(customer2.user_id)
                await db_postgres.set_matching_customers(customer1.user_id, customer1_matching)
