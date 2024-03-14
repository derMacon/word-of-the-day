from dataclasses import dataclass

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
                 input: str,
                 output: str,
                 deck: str = 'default',
                 dict_options_item_id: int = -1,
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
