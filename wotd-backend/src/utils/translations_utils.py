import dataclasses
from typing import Tuple, List

from src.data.data_types import Status, DictOptionsItem, DictOptionsResponse


def evaluate_status(original_input: str, options: List[DictOptionsItem]):
    if not options:
        return Status.NOT_FOUND
    elif not any(original_input.upper() == get_first_word_or_whole_text(option.input).upper() for option in options):
        # check if any lookup option is exactly equal to request input,
        # otherwise the input was misspelled
        return Status.MISSPELLED
    return Status.OK


def get_first_word_or_whole_text(text):
    words = text.split()
    if words:
        return words[0]
    else:
        return text

def asdict_nested(dict_options_response: DictOptionsResponse):
    options = []
    for curr_opt in dict_options_response.options:
        tmp = dataclasses.asdict(curr_opt)
        print("tmp: ", tmp)
        options.append(tmp)

    print("opts: ", options)
    output = dataclasses.asdict(dict_options_response)
    output['options'] = options

    return output
