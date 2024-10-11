from typing import List

from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.requeststatus import RequestStatus
from src.utils.logging_config import app_log

# TODO put this in ini file / db
TRANSLATION_DECK_PREFIX = 'wotd::translations'
DEFINITION_DECK = 'wotd_definitions'
PRESELECTED_ITEMS_COUNT = 2


def update_request_status(original_input: str, options: List[DictOptionsItem]):
    status: RequestStatus = RequestStatus.OK
    if not options:
        status = RequestStatus.NOT_FOUND
    elif not any(original_input.upper() == get_first_word_or_whole_text(option.input).upper() for option in options):
        # check if any lookup option is exactly equal to request input,
        # otherwise the input was misspelled
        status = RequestStatus.MISSPELLED

    for curr_option in options:
        curr_option.status = status

    app_log.debug(f'status: {status}')
    if status == RequestStatus.OK and options is not None:
        for i in range(min(len(options), PRESELECTED_ITEMS_COUNT)):
            options[i].selected = True  # preselect first n entries
            i += 1
    else:
        app_log.error(f'could not preselect items for the following status / options: {status} / {options}')


def update_deckname(options: List[DictOptionsItem], dict_request: DictRequest):
    deckname = f'{TRANSLATION_DECK_PREFIX}::{dict_request.from_language_uuid}-{dict_request.to_language_uuid}'
    for curr_option in options:
        curr_option.deck = deckname


def get_first_word_or_whole_text(text):
    words = text.split()
    if words:
        return words[0]
    else:
        return text
