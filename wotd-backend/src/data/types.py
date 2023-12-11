from dataclasses import dataclass
from enum import Enum


class Language(str, Enum):
    EN = "EN"
    DE = "DE"


class Status(str, Enum):
    NOT_FOUND = 'NOT_FOUND'
    MISSPELLED = 'MISSPELLED'
    OK = 'OK'

@dataclass
class InfoRequestAvailDictLang:
    dict_available_languages: [Language]

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
class DictOptionsResponse:
    id: int
    dict_request: DictRequest
    status: Status
    options: [Option]


@dataclass
class OptionSelectRequest:
    options_response_id: int
    selected_option_id: int


@dataclass
class DefRequest:
    language: Language
    word: str
