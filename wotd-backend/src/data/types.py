from dataclasses import dataclass
from enum import Enum


class LanguageShort(str, Enum):
    EN = "EN"
    # ENG = "ENG"
    DE = "DE"


class Status(str, Enum):
    NOT_FOUND = 'NOT_FOUND'
    MISSPELLED = 'MISSPELLED'
    OK = 'OK'


@dataclass
class Language:
    language_id: int
    name: str
    abbreviation: LanguageShort

    # translate enums when decoding json
    def __post_init__(self):
        if isinstance(self.abbreviation, str):
            self.abbreviation = LanguageShort(self.abbreviation.upper())


@dataclass
# TODO wouldn't the correct name be InfoResponseAvailDictLang
class InfoRequestAvailDictLang:
    dict_available_languages: [LanguageShort]


@dataclass
# TODO wouldn't the correct name be InfoResponseDefaultDictLang
class InfoRequestDefaultDictLang:
    dict_default_from_language: LanguageShort
    dict_default_to_language: LanguageShort


@dataclass
class DictRequest:
    from_language: LanguageShort
    to_language: LanguageShort
    input: str

    # translate enums when decoding json
    def __post_init__(self):
        if isinstance(self.from_language, str):
            self.from_language = LanguageShort(self.from_language.upper())
        if isinstance(self.to_language, str):
            self.to_language = LanguageShort(self.to_language.upper())


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
    language: LanguageShort
    word: str
