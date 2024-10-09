from dataclasses import dataclass
from typing import List, Dict

from src.data.anki import ANKI_CONNECT_VERSION
from src.data.anki.anki_card import AnkiCard


@dataclass
class AnkiConnectRequestDeleteNotes:
    action: str = 'deleteNotes'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, anki_card_ids: List[int]):
        self.params = {
            'notes': anki_card_ids
        }


@dataclass(frozen=True)
class AnkiConnectResponseDeleteNotes:
    result: str
    error: str
