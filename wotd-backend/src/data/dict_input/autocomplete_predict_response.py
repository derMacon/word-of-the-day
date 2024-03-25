from dataclasses import dataclass
from typing import List

from src.data.dict_input.autocomplete_predict_option import AutocompletePredictOption


@dataclass
class AutocompletePredictResponse:
    results: List[AutocompletePredictOption]
