from dataclasses import dataclass

from src.data.dict_input.language_uuid import LanguageUUID


@dataclass
class Language:
    language_uuid: LanguageUUID
    name: str

    # translate enums when decoding json
    def __post_init__(self):
        if isinstance(self.language_uuid, str):
            self.language_uuid = LanguageUUID(self.language_uuid.upper())
