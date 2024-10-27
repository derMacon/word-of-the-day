from dataclasses import dataclass
from typing import Dict

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass
class AnkiConnectRequestNotesInfo:
    action: str = 'notesInfo'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, anki_card_id: int):
        self.params = {
            'notes': [anki_card_id]
        }


@dataclass(frozen=True)
class AnkiConnectResponseNotesInfo:
    result: str
    error: str
