from dataclasses import dataclass

from src.data.dict_input.language_uuid import Language


@dataclass
class InfoResponseDefaultDictLang:
    dict_default_from_language: Language
    dict_default_to_language: Language
