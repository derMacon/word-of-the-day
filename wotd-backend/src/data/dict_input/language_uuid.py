from dataclasses import dataclass


@dataclass
class Language:
    language_uuid: str
    full_name: str
    enchant_key: str
