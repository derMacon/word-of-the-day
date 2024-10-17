from typing import List

import enchant
from singleton_decorator import singleton

from src.data.dict_input.language_uuid import Language
from src.data.error.lang_not_found_error import LangNotFoundError
from src.utils.logging_config import app_log

DEFAULT_RESULT_NUM = 10


@singleton
class DictTranslationService:

    def __init__(self, available_languages: List[Language]):
        app_log.debug(f'initialized dict translation service with languages: {available_languages}')
        self._dict_map = {
            member.language_uuid: enchant.Dict(member.enchant_key) for member in available_languages
        }

    def autocomplete(self, prefix: str, language_uuid: str) -> List[str]:
        app_log.debug(f"autocomplete '{prefix}' for language uuid string '{language_uuid}'")

        if prefix is None or len(prefix) == 0:
            return []

        if language_uuid not in self._dict_map.keys():
            raise LangNotFoundError(
                f"language '{language_uuid}' not present in available languages: '{self._dict_map.keys()}'")

        suggestions = self._dict_map[language_uuid].suggest(prefix)
        return [word for word in suggestions if word.startswith(prefix)][:DEFAULT_RESULT_NUM]
