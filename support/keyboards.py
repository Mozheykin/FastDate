from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    )

from config import LANGUAGES, GENDERS
from support.translate import translation, translate_prompt
from support.language import (CHANGE_LANGUAGE_M, 
                            LIKE, 
                            DISLIKE, 
                            MENU,
                            CHANGE_PROFILE,
                            MATCHING,
                            ADD_PHOTO,
                            BUY_GOLD)

kb = list()
for key, value in LANGUAGES.items():
    kb.append([InlineKeyboardButton(text=value, callback_data=key)])

keyboard_select_language  = InlineKeyboardMarkup(inline_keyboard=kb)

def get_gender_keyboard(language: str) -> ReplyKeyboardMarkup:
    kb_gender = list()
    geted_genders = GENDERS.get(language)
    if geted_genders is None:
        geted_genders_en = GENDERS.get('en')
        if geted_genders_en is not None:
            for key, value in geted_genders_en.items():
                geted_genders = {key: translation(language, value)}
    if isinstance(geted_genders, dict):
        for key, value in geted_genders.items():
            if value is not None and isinstance(value, str):
                kb_gender.append([KeyboardButton(text=value)])
    return ReplyKeyboardMarkup(keyboard=kb_gender, resize_keyboard=True, one_time_keyboard=True)

location_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Share location", request_location=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )

def get_matching_keyboard(language:str) -> ReplyKeyboardMarkup:
    text_like = translate_prompt(LIKE, language)
    text_dislike = translate_prompt(DISLIKE, language)
    main_menu = translate_prompt(MENU, language)
    return ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text=text_like), 
                        KeyboardButton(text=text_dislike) 
                        ],
                        [KeyboardButton(text=main_menu)],
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )

def get_main_menu_keyboard(language:str) -> ReplyKeyboardMarkup:
    # TODO add language 
    change_language = translate_prompt(CHANGE_LANGUAGE_M, language)
    change_profile = translate_prompt(CHANGE_PROFILE, language)
    matching = translate_prompt(MATCHING, language)
    add_photo = translate_prompt(ADD_PHOTO, language)
    buy_gold = translate_prompt(BUY_GOLD, language)
    return ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text=change_language),
                                KeyboardButton(text=change_profile),
                                KeyboardButton(text=matching)],
                                [KeyboardButton(text=add_photo),
                                KeyboardButton(text=buy_gold)]
                                ],
                    resize_keyboard=True,
                    one_time_keyboard=True)

# def get_menu_keyboard(language: str) -> ReplyKeyboardMarkup:
#     kb_menu = list()
#     text_menu = translate_prompt('MENU', language)
#     text_profile = translate_prompt('PROFILE', language)
#     text_matching = translate_prompt('MATCHING', language)
#     text_support = translate_prompt('SUPPORT', language)
#     kb_menu.append([KeyboardButton(text=text_menu)])