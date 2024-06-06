from typing import Optional
from asyncpg.connection import transaction
from deep_translator.google import GoogleTranslator
from config import length_message
from support.language import PROBLEM_LANGUAGE

def get_changs(text:str, len_chang:int=500) -> list:
    parts = list()
    while len(text) > 0:
        part = text[:len_chang]
        text = text[len_chang:]
        parts.append(part)
    return parts

def translation(translated: str, source:str="auto", 
                target:str="ru") -> Optional[str|list[str]]:
    translator = GoogleTranslator(source=source, target=target)
    if len(translated) > length_message:
        changs = get_changs(translated, length_message)
    else:
        changs = [translated]
    if len(changs) == 1:
        return translator.translate(changs[0])
    elif len(changs) > 1:
        result:list[str] = list()
        for chang in changs:
            result.append(translator.translate(chang))
        return result


def translate_prompt(PROMPT_DICT:dict, target:str="ru") -> str:
    if PROMPT_DICT[target] is not None:
        return PROMPT_DICT[target]
    else:
        en_text = PROMPT_DICT['en']
        if en_text is not None:
            translated = translation(en_text, source='en', target=target)
            if isinstance(translated, list):
                return translated[0]
            elif isinstance(translated, str):
                return translated
    return PROBLEM_LANGUAGE