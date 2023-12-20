from dataclasses import dataclass
from typing import List

from src.data.dict_input.language import Language


@dataclass
# TODO wouldn't the correct name be InfoResponseAvailDictLang
class InfoRequestAvailDictLang:
    dict_available_languages: List[Language]
