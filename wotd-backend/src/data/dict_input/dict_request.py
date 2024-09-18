from dataclasses import dataclass

from src.data.dict_input import now
from src.utils.logging_config import app_log


@dataclass
class DictRequest:
    dict_request_id: int
    from_language_uuid: str
    to_language_uuid: str
    input: str
    dict_request_ts: str

    def __init__(self, *args, **kwargs):
        if args:
            self.plain_read(args)
        else:
            self.generate_fields(kwargs)

    def plain_read(self, args):
        app_log.debug(f"args {args}")
        self.dict_request_id, self.user_id, self.from_language_uuid, self.to_language_uuid, self.input, self.dict_request_ts = args

    def generate_fields(self, kwargs):
        app_log.debug(f"constructor kwargs: {kwargs}")
        self.dict_request_id = None
        self.from_language_uuid = kwargs['from_language_uuid'].upper()
        self.to_language_uuid = kwargs['to_language_uuid'].upper()
        self.input = kwargs['input']
        self.dict_request_ts = now()
