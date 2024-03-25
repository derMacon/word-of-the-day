from typing import List

import requests

from src.utils.logging_config import app_log

AUTOCOMPLETE_API_SERVER_ADDRESS = 'https://api.imagineville.org'
AUTOCOMPLETE_API_BASE = AUTOCOMPLETE_API_SERVER_ADDRESS + '/word/predict'

DEFAULT_RESULT_NUM = 10


def lookup_autocomplete(prefix) -> List[str]:
    # TODO catch API error / API downtime etc.

    app_log.debug(f"prefix: '{prefix}'")

    data = {
        'prefix': prefix,
        'num': DEFAULT_RESULT_NUM
    }

    headers = {
        'Content-Type': 'application/json',  # Example header
    }

    response = requests.get(AUTOCOMPLETE_API_BASE, json=data)
    app_log.debug(f'response: {response}')
    return ['test1']
