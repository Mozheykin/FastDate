from aiogram.fsm.state import State, StatesGroup
from pydantic import BaseModel

class Form(StatesGroup):
    username = State()
    age = State()
    gender = State()
    language = State()
    info = State()
    photo = State()
    location = State()
    range = State()

class RegistrationCustomer(BaseModel):
    username: str
    age: int
    gender: str
    info: str
    photo: str
    location: str
    range: int