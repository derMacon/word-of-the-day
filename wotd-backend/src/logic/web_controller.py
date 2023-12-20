from typing import List

from dictcc import Dict

from src.data.data_types import DictRequest, DictOptionsResponse, Status, OptionSelectRequest, DictOptionsItem
from src.service.persistence_service import PersistenceService
from src.utils.logging_config import app_log
from src.utils.translations_utils import evaluate_status


class WebController:

    def __init__(self):
        self.dictcc_translator = Dict()
        self.persistence_service = PersistenceService()

    def lookup_dict_word(self, dict_request: DictRequest) -> DictOptionsResponse:

        response_tuples = self.dictcc_translator.translate(
            word=dict_request.input,
            from_language=dict_request.from_language_uuid.name.lower(),
            to_language=dict_request.to_language_uuid.name.lower()
        ).translation_tuples
        options: List[DictOptionsItem] = [DictOptionsItem(*curr_tuple) for curr_tuple in response_tuples]

        status: Status = evaluate_status(
            original_input=dict_request.input,
            options=options
        )

        dict_request = self.persistence_service.save_dict_unique_request(dict_request)
        app_log.debug(f"updated request: {dict_request}")

        dict_options_response = DictOptionsResponse(
            dict_request=dict_request,
            status=status,
            options=options
        )

        dict_options_response = self.persistence_service.save_dict_options_response(dict_options_response)

        return dict_options_response

    def select_dict_word(self, option_select_request: OptionSelectRequest) -> bool:
        app_log.debug(f"option_select_request: {option_select_request}")

        return True


controller = WebController()
