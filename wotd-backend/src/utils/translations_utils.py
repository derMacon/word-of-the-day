from typing import Tuple, List

from src.data.types import Status


def evaluate_status(original_input: str, options: List[Tuple[int, str, str]]):
    if not options:
        return Status.NOT_FOUND
    elif not any(option[1] == original_input for option in options):
        # check if any lookup option is exactly equal to request input,
        # otherwise the input was misspelled
        return Status.MISSPELLED


def add_id_to_tuples(data: List[Tuple[str, str]]) -> List[Tuple[int, str, str]]:
    new_data: List[Tuple[int, str, str]] = []

    for idx, item in enumerate(data, start=0):
        # idx is the ID, item is the original tuple
        new_item: Tuple[int, str, str] = (idx,) + item
        new_data.append(new_item)

    return new_data
