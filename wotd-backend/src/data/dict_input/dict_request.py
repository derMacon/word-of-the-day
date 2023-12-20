from dataclasses import dataclass

from src.data.dict_input import now
from src.data.dict_input.language_uuid import LanguageUUID
from src.utils.logging_config import app_log


@dataclass
class DictRequest:
    dict_request_id: int
    user_id: str
    from_language_uuid: LanguageUUID
    to_language_uuid: LanguageUUID
    input: str
    dict_request_ts: str

    def __init__(self, *args, **kwargs):
        if args:
            self.plain_read(args)
        else:
            self.generate_fields(kwargs)

    def plain_read(self, args):
        app_log.debug(f"args {args}")
        self.dict_request_id, self.user_id, from_language_uuid, to_language_uuid, self.input, self.dict_request_ts = args
        self.user_id = self.user_id.lower()
        self.from_language_uuid = LanguageUUID(from_language_uuid.upper())
        self.to_language_uuid = LanguageUUID(to_language_uuid.upper())

    def generate_fields(self, kwargs):
        app_log.debug(f"constructor kwargs: {kwargs}")
        self.dict_request_id = None
        self.user_id = kwargs['user_id'].lower()
        self.from_language_uuid = LanguageUUID(kwargs['from_language_uuid'].upper())
        self.to_language_uuid = LanguageUUID(kwargs['to_language_uuid'].upper())
        self.input = kwargs['input'].upper()
        self.dict_request_ts = now()
