from dictcc import Dict

from src.data.types import DictRequest, DictResponseOption, Status


class Controller:

    def __init__(self):
        self.translator = Dict()

    def lookup_word(self, dict_request: DictRequest) -> DictResponseOption:
        result = self.translator.translate(
            dict_request.input,
            from_language=dict_request.from_language.name.lower(),
            to_language=dict_request.to_language.name.lower()
        )

        options = result.translation_tuples

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


controller = Controller()
