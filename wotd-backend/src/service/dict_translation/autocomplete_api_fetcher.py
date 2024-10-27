from typing import List

import enchant

from src.utils.logging_config import app_log

AUTOCOMPLETE_API_SERVER_ADDRESS = 'https://api.imagineville.org'
AUTOCOMPLETE_API_BASE = AUTOCOMPLETE_API_SERVER_ADDRESS + '/word/predict'

DEFAULT_RESULT_NUM = 10


def lookup_autocomplete(prefix) -> List[str]:
    app_log.debug(f"prefix: '{prefix}'")
    d = enchant.Dict("en_US")
    suggestions = d.suggest(prefix)
    # Filter to only include words starting with the prefix (autocomplete behavior)
    return [word for word in suggestions if word.startswith(prefix)][:DEFAULT_RESULT_NUM]
