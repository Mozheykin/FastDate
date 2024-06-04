from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from models.registration import Form

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

    @router.message(Form.name)
    async def process_name(message: Message, state: FSMContext) -> None:
        await state.update_data(name=message.text)
        await state.set_state(Form.like_bots)
        await message.answer(
            f"Nice to meet you, {html.quote(message.text)}!\nDid you like to write bots?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Yes"),
                        KeyboardButton(text="No"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )


    @router.message(Form.like_bots, F.text.casefold() == "no")
    async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        await state.clear()
        await message.answer(
            "Not bad not terrible.\nSee you soon.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await show_summary(message=message, data=data, positive=False)


    @router.message(Form.like_bots, F.text.casefold() == "yes")
    async def process_like_write_bots(message: Message, state: FSMContext) -> None:
        await state.set_state(Form.language)

        await message.reply(
            "Cool! I'm too!\nWhat programming language did you use for it?",
            reply_markup=ReplyKeyboardRemove(),
        )


    @router.message(Form.like_bots)
    async def process_unknown_write_bots(message: Message) -> None:
        await message.reply("I don't understand you :(")


    @router.message(Form.language)
    async def process_language(message: Message, state: FSMContext) -> None:
        data = await state.update_data(language=message.text)
        await state.clear()

        if message.text.casefold() == "python":
            await message.reply(
                "Python, you say? That's the language that makes my circuits light up! 😉"
            )

        await show_summary(message=message, data=data)


    async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
        name = data["name"]
        language = data.get("language", "<something unexpected>")
        text = f"I'll keep in mind that, {html.quote(name)}, "
        text += (
            f"you like to write bots with {html.quote(language)}."
            if positive
            else "you don't like to write bots, so sad..."
        )
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

