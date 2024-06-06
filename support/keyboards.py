from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    )

from config import LANGUAGES



kb = list()
for key, value in LANGUAGES.items():
    kb.append([InlineKeyboardButton(text=value, callback_data='key')])

keyboard_select_language  = InlineKeyboardMarkup(inline_keyboard=kb)

location_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Share location", request_location=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )