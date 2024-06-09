import os  
from models.customer import Gender
BOT_TOKEN = os.getenv("BOT_TOKEN") 
DATABASE_URL = os.getenv("DATABASE_URL")  

DEFAULT_CUSTOMER = {
    'user_id': 0,                 
    'username': 'NoName',
    'balance': 100.0,                 
    'age': 0,                 
    'gender': Gender.male,                 
    'language': 'en',
    'info': 'NoInfo',                 
    'photo': 'NoPhoto',                 
    'location': '(12.33, 45.87)',
    'range': 500,                 
    'is_gold': True,
    'is_active': True,
}

length_message = 1000

LANGUAGES = {
    'ru': "🇷🇺 Russian 🇷🇺",
    'uk': "🇺🇦 Ukrainian 🇺🇦",
    'en': "🇺🇲 English 🇺🇲",
}

GENDERS = {
    'ru': {
        'male': "👨 Мужской 👨",
        'female': "👩 Женский 👩",
    },
    'uk': {
        'male': "👨 Мужскій 👨",
        'female': "👩 Жіночий 👩",
    },
    'en': {
        'male': "👨 Male 👨",
        'female': "👩 Female 👩",
    }
}