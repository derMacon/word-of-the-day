from dataclasses import dataclass
from enum import Enum, auto

from src.utils.logging_config import app_log


class Language(str, Enum):
    EN = "EN"
    DE = "DE"


class Status(str, Enum):
    NOT_FOUND = 'NOT_FOUND'
    MISSPELLED = 'MISSPELLED'
    OK = 'OK'


@dataclass
class DictRequest:
    from_language: Language
    to_language: Language
    input: str

    # translate enums when decoding json
    def __post_init__(self):
        if isinstance(self.from_language, str):
            self.from_language = Language(self.from_language.upper())
        if isinstance(self.to_language, str):
            self.to_language = Language(self.to_language.upper())


@dataclass
class Option:
    id: int
    input: str
    output: str


@dataclass
class DictResponseOption:
    dict_request: DictRequest
    status: Status
    options: [Option]


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
