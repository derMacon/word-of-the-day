from typing import Tuple, List

from src.data.types import Status, Option


def evaluate_status(original_input: str, options: List[Option]):
    if not options:
        return Status.NOT_FOUND
    elif not any(option.input == original_input for option in options):
        # check if any lookup option is exactly equal to request input,
        # otherwise the input was misspelled
        return Status.MISSPELLED
    return Status.OK


def add_id_to_tuples(data: List[Tuple[str, str]]) -> List[Option]:
    new_data: List[Option] = []

    for idx, item in enumerate(data, start=0):
        # idx is the ID, item is the original tuple
        new_data.append(Option(
            id=idx,
            input=item[0],
            output=item[1]
        ))

    return new_data
