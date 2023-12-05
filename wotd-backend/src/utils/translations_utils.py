from typing import Tuple, List

from src.data.types import Status


def evaluate_status(original_input: str, options: List[Tuple[str, str]]):
    if not options:
        return Status.NOT_FOUND
    elif not any(option[0] == original_input for option in options):
        # check if any lookup option is exactly equal to request input,
        # otherwise the input was misspelled
        return Status.MISSPELLED

