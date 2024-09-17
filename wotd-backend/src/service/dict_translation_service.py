from typing import List

import enchant
from singleton_decorator import singleton

from src.data.dict_input.language_uuid import LanguageUUID
from src.data.error.lang_not_found_error import LangNotFoundError

DEFAULT_RESULT_NUM = 10


@singleton
class DictTranslationService:

    def __init__(self):
        self._dict_map = {member: enchant.Dict(member.enchant_key) for member in LanguageUUID}

    def autocomplete(self, prefix: str, language: LanguageUUID) -> List[str]:
        if language not in self._dict_map.keys():
            raise LangNotFoundError(f"cannot autocomplete prefix '{prefix}' for language '{language}'")

        suggestions = self._dict_map[language].suggest(prefix)
        return [word for word in suggestions if word.startswith(prefix)][:DEFAULT_RESULT_NUM]
