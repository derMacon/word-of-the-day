from dataclasses import dataclass
from enum import Enum

from src.utils.logging_config import app_log


class LanguageUUID(str, Enum):
    EN = "EN"
    DE = "DE"


class Status(str, Enum):
    NOT_FOUND = 'NOT_FOUND'
    MISSPELLED = 'MISSPELLED'
    OK = 'OK'


@dataclass
class Language:
    language_uuid: LanguageUUID
    name: str

    # translate enums when decoding json
    def __post_init__(self):
        if isinstance(self.language_uuid, str):
            self.language_uuid = LanguageUUID(self.language_uuid.upper())


@dataclass
# TODO wouldn't the correct name be InfoResponseAvailDictLang
class InfoRequestAvailDictLang:
    dict_available_languages: [LanguageUUID]


@dataclass
# TODO wouldn't the correct name be InfoResponseDefaultDictLang
class InfoRequestDefaultDictLang:
    dict_default_from_language: LanguageUUID
    dict_default_to_language: LanguageUUID


@dataclass
class DictRequest:
    dict_request_id: int
    from_language_uuid: LanguageUUID
    to_language_uuid: LanguageUUID
    input: str

    def __init__(self, *args, **kwargs):
        if args:
            self.dict_request_id, from_language_uuid, to_language_uuid, self.input = args
            self.from_language_uuid = LanguageUUID(from_language_uuid.upper())
            self.to_language_uuid = LanguageUUID(to_language_uuid.upper())
        else:
            app_log.debug(f"constructor kwargs: {kwargs}")
            self.dict_request_id = None
            self.from_language_uuid = LanguageUUID(kwargs['from_language_uuid'].upper())
            self.to_language_uuid = LanguageUUID(kwargs['to_language_uuid'].upper())
            self.input = kwargs['input']


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
    language: LanguageUUID
    word: str
