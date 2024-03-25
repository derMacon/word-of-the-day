from dataclasses import dataclass
from typing import List

from src.data.dict_input.autocomplete_predict_option import AutocompletePredictOption


@dataclass
class AutocompletePredictResponse:
    results: List[AutocompletePredictOption]

    def __post_init__(self):
        if isinstance(self.results, list):
            parsed_options: List[AutocompletePredictOption] = []
            for curr_item in self.results:
                parsed_options.append(AutocompletePredictOption(**curr_item))
            self.results = parsed_options
