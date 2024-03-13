from typing import List

from dictcc import Dict

from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_options_response import DictOptionsResponse
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.option_select_request import OptionSelectRequest
from src.data.dict_input.status import Status
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
        app_log.debug(f'lookup options: {options}')

        status: Status = evaluate_status(
            original_input=dict_request.input,
            options=options
        )
        app_log.debug(f'status: {status}')
        if status == Status.OK and options is not None and options:
            options[0].selected = True  # preselect first entry

        dict_options_response = DictOptionsResponse(
            status=status,
            options=options
        )

        dict_options_response = self.persistence_service.save_dict_options_response(dict_options_response)
        app_log.debug(f'persisted dict options: {dict_options_response}')

        return dict_options_response

    def select_dict_word(self, item_id: int) -> bool:
        app_log.debug(f"toggle item id: {item_id}")
        self.persistence_service.update_selected_item(item_id)
        return True


controller = WebController()
