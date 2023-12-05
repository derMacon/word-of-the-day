from dictcc import Dict

from src.data.types import DictRequest, DictResponseOption, Status
from src.utils.logging_config import app_log


class Controller:

    def __init__(self):
        self.dictcc_translator = Dict()

    def lookup_word(self, dict_request: DictRequest) -> DictResponseOption:
        result = self.dictcc_translator.translate(
            dict_request.input,
            from_language=dict_request.from_language.name.lower(),
            to_language=dict_request.to_language.name.lower()
        )

        options = result.translation_tuples

        app_log.debug(f"response options: {options}")

        status = Status.OK
        if not options:
            status = Status.NOT_FOUND
        elif not any(option[0] == dict_request.input for option in options):
            # check if any lookup option is exactly equal to request input,
            # otherwise the input was misspelled
            status = Status.MISSPELLED

        return DictResponseOption(
            dict_request=dict_request,
            status=status,
            options=options
        )

        # return None


controller = Controller()
