import logging 
import asyncio
import sys
from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery, ContentType, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from support.language import (ACTIVATE_MESSAGE, 
                        CHANGE_LANGUAGE, 
                        DEACTIVATE_MESSAGE, 
                        DELETE_MESSAGE, 
                        GOLD_MESSAGE, REG_AGE, REG_GENDER, REG_INFO, REG_LOCATION, REG_NAME, REG_PHOTO, REG_RANGE, 
                        START_MESSAGE)
from models.customer import Customer, CustomerView
from db import DB 
from support.keyboards import get_gender_keyboard, keyboard_select_language
# from handlers import matching, profile, support  
from config import BOT_TOKEN, DEFAULT_CUSTOMER, DATABASE_URL, LANGUAGES
from support.translate import translate_prompt
from support.keyboards import location_keyboard
from models.registration import Form, RegistrationCustomer

dp = Dispatcher()  
form_router = Router()
logo_mp4 = FSInputFile('media/logo.MP4')
bot = None
db_postgres = DB()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    default_customer = Customer(**DEFAULT_CUSTOMER)
    default_customer.user_id = message.chat.id
    if message.from_user is None:
        full_name = 'None'
    else:
        full_name = message.from_user.full_name
    default_customer.username = full_name
    geted_customer = await db_postgres.get_customer(default_customer.user_id)
    if  geted_customer is None:
        language = default_customer.language
        await db_postgres.add_customer(default_customer)
        start_message = translate_prompt(START_MESSAGE, language)
        await message.answer_video(logo_mp4)
        await message.answer(start_message, reply_markup=keyboard_select_language)
    else:
        default_customer = CustomerView(**geted_customer)
        language = default_customer.language
        if default_customer.is_active is not True:
            activate_message = translate_prompt(DEACTIVATE_MESSAGE, language) 
            await db_postgres.activate_customer(default_customer.user_id)
            await message.reply(activate_message, reply_markup=keyboard_select_language)
        else:
            activate_message = translate_prompt(ACTIVATE_MESSAGE, language) 
            await message.reply(activate_message)
            
@dp.message(Command('delete'))
async def delete_customer(message: Message):
    _id = message.chat.id
    get_user = await db_postgres.get_customer(_id)
    if get_user is not None:
        deleted_customer = CustomerView(**get_user)
        language = deleted_customer.language
        await db_postgres.deactivate_customer(_id)
        deleted_message = translate_prompt(DELETE_MESSAGE, language) 
        await message.reply(deleted_message)

@dp.message(Command('registration', 'change'))
@dp.message(F.text.casefold() == 'registration')
async def registration_customer(message: Message, state: FSMContext):
    customer = await db_postgres.get_customer(message.chat.id)
    if customer is not None:
        def_customer = CustomerView(**customer)
        language = def_customer.language
        name_message = translate_prompt(REG_NAME, language)
        await state.update_data(language=language)
        await state.set_state(Form.username)
        await message.answer(name_message)

@dp.message(Form.username)
async def process_username(message: Message, state: FSMContext) -> None:
    data = await state.update_data(username=message.text)
    await state.set_state(Form.age)
    language = data.get('language', 'en')
    age_message = translate_prompt(REG_AGE, language)
    await message.answer(age_message)

@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext) -> None:
    if message.text is not None and message.text.isdigit():
        age = int(message.text)
        if 18 < age < 75:
            data = await state.update_data(age=age)
            language = data.get('language', 'en')
            gender_message = translate_prompt(REG_GENDER, language)
            await state.set_state(Form.gender)
            customer = await db_postgres.get_customer(message.chat.id)
            if customer is not None:
                customerview = CustomerView(**customer)
                kb_gender = get_gender_keyboard(customerview.language)
                await message.answer(gender_message, reply_markup=kb_gender)

@dp.message(Form.gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    data = await state.update_data(gender=message.text)
    language = data.get('language', 'en')
    info_message = translate_prompt(REG_INFO, language)
    await state.set_state(Form.info)
    await message.answer(info_message)

@dp.message(Form.info)
async def process_info(message: Message, state: FSMContext) -> None:
    data = await state.update_data(info=message.text)
    language = data.get('language', 'en')
    photo_message = translate_prompt(REG_PHOTO, language)
    await state.set_state(Form.photo)
    await message.answer(photo_message)
    # Слать несколько фото

@dp.message(Form.photo, F.content_type.in_({ContentType.PHOTO, ContentType.VIDEO}))
async def process_photo(message: Message, state: FSMContext) -> None:
    if message.photo is not None:
        photo_id = message.photo[-1].file_id
        data = await state.update_data(photo=photo_id)
        language = data.get('language', 'en')
        location_message = translate_prompt(REG_LOCATION, language)
        await state.set_state(Form.location)
        await message.answer(
            location_message,
            reply_markup=location_keyboard,
        )

@dp.message(Form.location, F.content_type == ContentType.LOCATION)
async def process_location(message: Message, state: FSMContext) -> None:
    if message.location is not None:
        location = message.location
        data = await state.update_data(location=f"{location.latitude}, {location.longitude}")
        language = data.get('language', 'en')
        range_message = translate_prompt(REG_RANGE, language)
        await state.set_state(Form.range)
        await message.answer(range_message, reply_markup=ReplyKeyboardRemove())

@dp.message(Form.range)
async def process_range(message: Message, state: FSMContext) -> None:
    try:
        if message.text is not None:
            range_val = float(message.text)
        else:
            range_val = 500
    except ValueError:
        await message.reply("Invalid range. Enter a numeric value.")
        return
    data = await state.update_data(range=range_val)
    registration_customer = RegistrationCustomer(**data)
    # TODO вставить проверку, на значения внутри БД, есл иравны, то пропускать замену
    # В идеале переписать 1 функцией, чтоб было меньше вызовов
    await db_postgres.change_customer('username', registration_customer.username, message.chat.id)
    await db_postgres.change_customer('age', registration_customer.age, message.chat.id)
    await db_postgres.change_customer('gender', registration_customer.gender, message.chat.id)
    await db_postgres.change_customer('info', registration_customer.info, message.chat.id)
    await db_postgres.change_customer('photo', registration_customer.photo, message.chat.id)
    # TODO выгружатль фото
    await db_postgres.change_customer('location', registration_customer.location, message.chat.id)
    await db_postgres.change_customer('range', registration_customer.range, message.chat.id)
    await message.answer("Registration complete!")
    await state.clear() 
# {'username': 'Дмитрий', 'age': 25, 'gender': 'Male', 'info': 'Привет', 'photo': 'AgACAgIAAxkBAAOPZmIUDJWSGAABydjvzfRh-g8OQLI1AAJn3zEbwu4RS1Hxpv-Pffs1AQADAgADeQADNQQ', 'location': '55.759443, 37.692032', 'range': 500.0}

@dp.message(Command('gold'))
async def set_gold_status(message: Message):
    _id = message.chat.id
    get_user = await db_postgres.get_customer(_id)
    if get_user is not None:
        gold_ch_customer = CustomerView(**get_user)
        language = gold_ch_customer.language
        # TODO Добавить списание со счёта или сразу на оплату, пока так 
        await db_postgres.set_gold_status(_id)
        gold_message = translate_prompt(GOLD_MESSAGE, language) 
        await message.reply(gold_message)

@dp.callback_query()
async def change_language_to_ru(call: CallbackQuery):
    _id = call.from_user.id
    match call.data:
        case lang if lang in LANGUAGES:
            await db_postgres.change_language(_id, lang)
            answer = translate_prompt(CHANGE_LANGUAGE, lang) 
            await call.message.answer(text=answer) # pyright: ignore

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        pass
        # await message.send_copy(chat_id=message.chat.id)
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
    await db_postgres.init_pool()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":     
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print(f'[INFO] {DATABASE_URL=}')
    print(f'[INFO] {BOT_TOKEN=}')
    asyncio.run(main())