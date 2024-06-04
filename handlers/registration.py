from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from models.registration import Form
from models.customer import Customer

async def registration(router:Router):
    # TODO изменить заполнение по своей форме
    @router.message(Command("cancel"))
    @router.message(F.text.casefold() == "cancel")
    async def cancel_handler(message: Message, state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.clear()
        await message.answer(
            "Cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )

    @router.message(Form.username)
    async def process_username(message: Message, state: FSMContext) -> None:
        await state.update_data(username=message.text)
        await state.set_state(Form.age)
        await message.answer("Enter your age:")

    @router.message(Form.age)
    async def process_age(message: Message, state: FSMContext) -> None:
        try:
            if message.text is not None:
                age = int(message.text)
            else:
                age = 18
        except ValueError:
            await message.reply("Invalid age. Enter an integer value.")
            return
        await state.update_data(age=age)
        await state.set_state(Form.gender)
        await message.answer("Enter your gender:")

    @router.message(Form.gender)
    async def process_gender(message: Message, state: FSMContext) -> None:
        await state.update_data(gender=message.text)
        await state.set_state(Form.language)
        await message.answer("Enter your language:")

    @router.message(Form.language)
    async def process_language(message: Message, state: FSMContext) -> None:
        await state.update_data(language=message.text)
        await state.set_state(Form.info)
        await message.answer("Enter additional info:")

    @router.message(Form.info)
    async def process_info(message: Message, state: FSMContext) -> None:
        await state.update_data(info=message.text)
        await state.set_state(Form.photo)
        await message.answer("Send your photo:")

    @router.message(Form.photo, content_types=ContentType.PHOTO)
    async def process_photo(message: Message, state: FSMContext) -> None:
        if message.photo is not None:
            photo_id = message.photo[-1].file_id
            await state.update_data(photo=photo_id)
        await state.set_state(Form.location)
        await message.answer(
            "Please share your location:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Share location", request_location=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

    @router.message(Form.location, content_types=ContentType.LOCATION)
    async def process_location(message: Message, state: FSMContext) -> None:
        if message.location is not None:
            location = message.location
            await state.update_data(location=f"{location.latitude}, {location.longitude}")
        await state.set_state(Form.range)
        await message.answer("Enter your range:", reply_markup=ReplyKeyboardRemove())

    @router.message(Form.range)
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
        updated_customer = Customer(**data)
        # TODO записать в БД