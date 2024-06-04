from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    username = State()
    age = State()
    gender = State()
    language = State()
    info = State()
    photo = State()
    location = State()
    range = State()