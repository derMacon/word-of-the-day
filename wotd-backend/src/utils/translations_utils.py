from typing import List

from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.status import Status
from src.utils.logging_config import app_log

# TODO put this into .ini file
TRANSLATION_DECK = 'wotd_translations'
DEFINITION_DECK = 'wotd_definitions'
PRESELECTED_ITEMS_COUNT = 2


def update_status(original_input: str, options: List[DictOptionsItem]):
    status: Status = Status.OK
    if not options:
        status = Status.NOT_FOUND
    elif not any(original_input.upper() == get_first_word_or_whole_text(option.input).upper() for option in options):
        # check if any lookup option is exactly equal to request input,
        # otherwise the input was misspelled
        status = Status.MISSPELLED

    for curr_option in options:
        curr_option.status = status

    app_log.debug(f'status: {status}')
    if (status == Status.OK
            and options is not None
            and len(options) >= PRESELECTED_ITEMS_COUNT):
        for i in range(PRESELECTED_ITEMS_COUNT):
            options[i].selected = True  # preselect first n entries
            i += 1
    else:
        app_log.error(f'could not preselect items for the following status / options: {status} / {options}')


def update_deckname(options: List[DictOptionsItem], dict_request: DictRequest):
    # TODO delete this
    # to_lang: Language = persistence_service.find_language_by_uuid(dict_request.to_language_uuid)
    # from_lang: Language = persistence_service.find_language_by_uuid(dict_request.from_language_uuid)

    deckname = TRANSLATION_DECK
    if dict_request.to_language_uuid == dict_request.from_language_uuid:
        app_log.debug('from and to language of lookup request are the same '
                      '- just search for definition of word, not for translation')
        deckname = DEFINITION_DECK

    app_log.debug('generated deckname: %s', deckname)
    for curr_option in options:
        curr_option.deck = deckname


def get_first_word_or_whole_text(text):
    words = text.split()
    if words:
        return words[0]
    else:
        return text
