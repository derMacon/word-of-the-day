from dataclasses import dataclass
from typing import List

from src.data.dict_input.language_uuid import Language


@dataclass
class InfoResponseAvailDictLang:
    dict_available_languages: List[Language]
