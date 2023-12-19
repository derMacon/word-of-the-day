from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import List

from src.utils.logging_config import app_log

DATETIME_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'
BERLIN_TIMEZONE = timezone(timedelta(hours=1))

def now():
    return datetime.now(BERLIN_TIMEZONE).strftime(DATETIME_FORMAT_STRING)

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
    dict_available_languages: List[Language]


@dataclass
# TODO wouldn't the correct name be InfoResponseDefaultDictLang
class InfoRequestDefaultDictLang:
    dict_default_from_language: Language
    dict_default_to_language: Language


@dataclass
class DictRequest:
    dict_request_id: int
    from_language_uuid: LanguageUUID
    to_language_uuid: LanguageUUID
    input: str
    ts: str

    def __init__(self, *args, **kwargs):
        if args:
            self.plain_read(args)
        else:
            self.generate_fields(kwargs)

    def plain_read(self, args):
        app_log.debug(f"args {args}")
        self.dict_request_id, from_language_uuid, to_language_uuid, self.input, self.ts = args
        self.from_language_uuid = LanguageUUID(from_language_uuid.upper())
        self.to_language_uuid = LanguageUUID(to_language_uuid.upper())

    def generate_fields(self, kwargs):
        app_log.debug(f"constructor kwargs: {kwargs}")
        self.dict_request_id = None
        self.from_language_uuid = LanguageUUID(kwargs['from_language_uuid'].upper())
        self.to_language_uuid = LanguageUUID(kwargs['to_language_uuid'].upper())
        self.input = kwargs['input'].upper()
        self.ts = now() # TODO rename dict_request_ts


@dataclass
class DictOptionsItem:
    dict_options_item_id: int
    dict_options_response_id: int
    input: str
    output: str

    def __init__(self,
                 input: str,
                 output: str,
                 dict_options_response_id: int = -1,
                 option_id: int = -1):
        self.option_id = option_id
        self.dict_options_response_id = dict_options_response_id
        self.input = input.replace("'", "")
        self.output = output.replace("'", "")

@dataclass
class DictOptionsResponse:
    dict_options_response_id: int
    dict_request: DictRequest
    status: Status
    options: List[DictOptionsItem]
    options_response_ts: str

    def __init__(self,
                 dict_request: DictRequest,
                 status: Status,
                 options: List[DictOptionsItem],
                 dict_options_response_id: int = -1,
                 ts: str = now()):
        self.dict_options_response_id: int = dict_options_response_id
        self.dict_request: DictRequest = dict_request
        self.status: Status = status
        self.options: List[DictOptionsItem] = options
        self.options_response_ts: str = ts

@dataclass
class OptionSelectRequest:
    options_response_id: int
    selected_option_id: int

@dataclass
class DefRequest:
    language: LanguageUUID
    word: str
