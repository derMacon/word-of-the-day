from dataclasses import dataclass


@dataclass
class DictOptionsItem:
    dict_options_item_id: int
    dict_options_response_id: int
    input: str
    output: str

    def __init__(self,
                 input: str,
                 output: str,
                 dict_options_response_id: int = -1,
                 dict_options_item_id: int = -1):
        self.dict_options_item_id = dict_options_item_id
        self.dict_options_response_id = dict_options_response_id
        self.input = input.replace("'", "")
        self.output = output.replace("'", "")
