from dataclasses import dataclass
from typing import List

from src.data.dict_input import now
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.status import Status


@dataclass
class DictOptionsResponse:
    dict_options_response_id: int
    status: Status
    options: List[DictOptionsItem]
    options_response_ts: str

    def __init__(self,
                 status: Status,
                 options: List[DictOptionsItem],
                 dict_options_response_id: int = -1,
                 ts: str = now()):
        self.dict_options_response_id: int = dict_options_response_id
        self.status: Status = status
        self.options: List[DictOptionsItem] = options
        self.options_response_ts: str = ts
