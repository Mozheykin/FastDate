import os  

BOT_TOKEN = os.getenv("BOT_TOKEN") 
DATABASE_URL = os.getenv("DATABASE_URL")  
LANGUAGES = {
    'ru': 'Русский',
    'uk': 'Український', 
    'en': 'English',
}

DEFAULT_CUSTOMER = {
    'user_id': 0,                 
    'username': 'NoName',
    'balance': 100.0,                 
    'age': 0,                 
    'gender': 'male',                 
    'language': 'ru',
    'info': 'NoInfo',                 
    'photo': 'NoPhoto',                 
    'location': '(12.33, 45.87)',
    'range': 500,                 
    'is_gold': True,
    'is_active': True,
}