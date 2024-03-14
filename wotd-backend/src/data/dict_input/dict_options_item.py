from dataclasses import dataclass
from typing import List

from src.data.dict_input import now
from src.data.dict_input.status import Status


@dataclass
class DictOptionsItem:
    dict_options_item_id: int
    deck: str
    input: str
    output: str
    selected: bool
    status: Status
    option_response_ts: str

    def __init__(self,
                 dict_options_item_id: int = -1,
                 deck: str = '',
                 input: str = '',
                 output: str = '',
                 selected: bool = False,
                 status: Status = Status.OK,
                 ts: str = now()):
        self.dict_options_item_id = dict_options_item_id
        self.input = input.replace("'", "")
        self.output = output.replace("'", "")
        self.deck: str = deck
        self.selected = selected
        self.status = status
        self.option_response_ts = ts


def from_translation_tuples(response_tuples) -> List[DictOptionsItem]:
    # TODO types in signature
    parsed_options: List[DictOptionsItem] = []
    for curr_tuple in response_tuples:
        item: DictOptionsItem = DictOptionsItem(
            input=curr_tuple[0],
            output=curr_tuple[1],
        )
        parsed_options.append(item)

    return parsed_options
