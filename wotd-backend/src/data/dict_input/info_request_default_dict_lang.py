from dataclasses import dataclass

from src.data.dict_input.language import Language


@dataclass
# TODO wouldn't the correct name be InfoResponseDefaultDictLang
class InfoRequestDefaultDictLang:
    dict_default_from_language: Language
    dict_default_to_language: Language
