from dataclasses import dataclass
from typing import List

from src.data.dict_input import now
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.dict_input.requeststatus import RequestStatus
from src.utils.logging_config import app_log


@dataclass
class DictOptionsItem:
    dict_options_item_id: int
    username: str
    deck: str
    input: str
    output: str
    selected: bool
    status: RequestStatus
    option_response_ts: str

    def __init__(self,
                 dict_options_item_id: int = -1,
                 username: str = '',
                 deck: str = '',
                 input: str = '',
                 output: str = '',
                 selected: bool = False,
                 status: RequestStatus = RequestStatus.OK,
                 ts: str = now()):
        self.dict_options_item_id = dict_options_item_id
        self.input = input.replace("'", "")
        self.output = output.replace("'", "")
        self.username: str = username
        self.deck: str = deck
        self.selected = selected
        self.status = status
        self.option_response_ts = ts


def from_translation_tuples(response_tuples, auth_headers: UnsignedAuthHeaders | None) -> List[DictOptionsItem]:
    app_log.debug('translating tuples')
    username = '' if auth_headers is None else auth_headers.username
    parsed_options: List[DictOptionsItem] = []
    for curr_tuple in response_tuples:
        item: DictOptionsItem = DictOptionsItem(
            input=curr_tuple[0],
            output=curr_tuple[1],
            username=username,
            ts=now()
        )

        parsed_options.append(item)

    return parsed_options
