import os  

BOT_TOKEN = os.getenv("BOT_TOKEN") 
DATABASE_URL = os.getenv("DATABASE_URL")  
LANGUAGES = {
    'ru': 'Русский',
    'uk': 'Український', 
    'en': 'English',
}

DEFAULT_PROFILE = {
    'language': 'ru',
    'range': 500,
    'balance': 100.0,
    'is_gold': True,
}