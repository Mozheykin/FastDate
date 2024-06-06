from typing import Optional
from deep_translator.google import GoogleTranslator
from config import length_message

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