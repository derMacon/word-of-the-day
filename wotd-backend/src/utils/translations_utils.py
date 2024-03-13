import dataclasses
from typing import List

from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.status import Status
from src.utils.logging_config import app_log


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
    if status == Status.OK and options is not None and options:
        options[0].selected = True  # preselect first entry


def get_first_word_or_whole_text(text):
    words = text.split()
    if words:
        return words[0]
    else:
        return text
