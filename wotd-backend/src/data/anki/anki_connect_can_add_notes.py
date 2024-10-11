from dataclasses import dataclass
from typing import Dict

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass
class AnkiConnectRequestCanAddNotes:
    action: str = 'canAddNotes'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, anki_cards):
        self.params = {
            'notes': [
                card.to_anki_connect_params_format() for card in anki_cards
            ]
        }


@dataclass(frozen=True)
class AnkiConnectResponseCanAddNotes:
    result: str
    error: str
