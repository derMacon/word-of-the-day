from typing import Tuple, List

from src.data.data_types import Status, DictOptionsItem


def evaluate_status(original_input: str, options: List[DictOptionsItem]):
    if not options:
        return Status.NOT_FOUND
    elif not any(original_input.upper() in option.input.upper() for option in options):
        # check if any lookup option is exactly equal to request input,
        # otherwise the input was misspelled
        return Status.MISSPELLED
    return Status.OK
