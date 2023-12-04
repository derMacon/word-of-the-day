from enum import Enum, auto

from src.utils.logging_config import app_log


class Language(Enum):
    EN = auto()
    DE = auto()


class Status(Enum):
    NOT_FOUND = auto()
    MISSPELLED = auto()
    OK = auto()


class DictRequest:
    def __init__(self, from_language: Language, to_language: Language, input: str):
        self.from_language = from_language
        self.to_language = to_language
        self.input = input

    def to_map(self):
        return {
            'from_language': self.from_language.name,
            'to_language': self.to_language.name,
            'input': self.input,
        }


class DictResponseOption:

    def __init__(self, dict_request: DictRequest, status: Status, options: [str]):
        self.dict_request = dict_request
        self.status = status
        self.options = options

    def to_map(self):
        return {
            'dict_request': self.dict_request.to_map(),
            'status': self.status.name,
            'options': str(self.options),
        }


class DictResponseSelect:
    def __init__(self, dict_response_options: DictResponseOption, selected_word: str):
        self.dict_response_options = dict_response_options
        self.selected_word = selected_word


def translate_dict_request(request_data: dict[str, str]) -> DictRequest:
    try:
        input = request_data['input']
        from_language_str = request_data['from_language']
        to_language_str = request_data['to_language']
    except KeyError:
        msg = f"invalid input data: {request_data}"
        app_log.error(msg)
        raise Exception(msg)

    from_language = None
    to_language = None
    for member in Language:
        if from_language_str.upper() == member.name:
            from_language = member
        if to_language_str.upper() == member.name:
            to_language = member

    if from_language is None or to_language is None:
        msg = (f"on of the given input languages is not supported, "
               f"from_language: {from_language}; to_language: {to_language}")
        app_log.error(msg)
        raise Exception(msg)

    return DictRequest(input=input, from_language=from_language, to_language=to_language)


class DefRequest:

    def __init__(self, language: Language, word: str):
        self.language = language
        self.word = word
