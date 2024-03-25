import json
from typing import List

import requests

from src.data.dict_input.autocomplete_predict_response import AutocompletePredictResponse
from src.utils.logging_config import app_log

AUTOCOMPLETE_API_SERVER_ADDRESS = 'https://api.imagineville.org'
AUTOCOMPLETE_API_BASE = AUTOCOMPLETE_API_SERVER_ADDRESS + '/word/predict'

DEFAULT_RESULT_NUM = 10


def lookup_autocomplete(prefix) -> List[str]:
    # TODO catch API error / API downtime etc.

    app_log.debug(f"prefix: '{prefix}'")

    params = {
        'prefix': prefix,
        'num': DEFAULT_RESULT_NUM
    }

    plain_response = requests.get(AUTOCOMPLETE_API_BASE, params=params).json()
    app_log.debug(f'plain response: {plain_response}')

    parsed_response: AutocompletePredictResponse = AutocompletePredictResponse(**plain_response)
    app_log.debug(f'parsed response: {parsed_response}')

    output = [curr_prediction.text for curr_prediction in parsed_response.results]
    app_log.debug(f'plain words: {output}')

    return output
