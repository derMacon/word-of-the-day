from dictcc import Dict

from src.data.types import DictRequest, DictOptionsResponse, Status, OptionSelectRequest, Option
from src.service.persistence_service import PersistenceService
from src.utils.logging_config import app_log
from src.utils.translations_utils import evaluate_status, add_id_to_tuples


class Controller:

    def __init__(self):
        self.dictcc_translator = Dict()
        self.persistence_service = PersistenceService()

    def lookup_dict_word(self, dict_request: DictRequest) -> DictOptionsResponse:

        response_tuples = self.dictcc_translator.translate(
            word=dict_request.input,
            from_language=dict_request.from_language_uuid.name.lower(),
            to_language=dict_request.to_language_uuid.name.lower()
        ).translation_tuples
        options: [Option] = add_id_to_tuples(response_tuples)
        app_log.debug(f"response options: {options}")

        status: Status = evaluate_status(
            original_input=dict_request.input,
            options=options
        )

        dict_request = self.persistence_service.save_dict_request(dict_request)

        dict_options_response = DictOptionsResponse(
            id=dict_request.dict_request_id,
            dict_request=dict_request,
            status=status,
            options=options
        )

        if status == Status.OK:
            self.persistence_service.save_dict_options_response(
                entry_id=dict_request.dict_request_id,
                dict_options_response=dict_options_response
            )

        return dict_options_response

    def select_dict_word(self, option_select_request: OptionSelectRequest) -> bool:
        app_log.debug(f"option_select_request: {option_select_request}")

        return True


controller = Controller()
