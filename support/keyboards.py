from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    )

from config import LANGUAGES, GENDERS
from support.translate import translation

kb = list()
for key, value in LANGUAGES.items():
    kb.append([InlineKeyboardButton(text=value, callback_data='key')])

keyboard_select_language  = InlineKeyboardMarkup(inline_keyboard=kb)

def get_gender_keyboard(language: str) -> ReplyKeyboardMarkup:
    kb_gender = list()
    geted_genders = GENDERS[language]
    if geted_genders is None:
        geted_genders_en = GENDERS['en']
        for key, value in geted_genders_en.items():
            geted_genders[key] = translation(language, value)
    for key, value in geted_genders.items():
        kb_gender.append([KeyboardButton(text=value)])
    return ReplyKeyboardMarkup(keyboard=kb_gender, resize_keyboard=True, one_time_keyboard=True)

location_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Share location", request_location=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )