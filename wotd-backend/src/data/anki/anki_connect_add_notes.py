from dataclasses import dataclass
from typing import List, Dict

from src.data.anki import ANKI_CONNECT_VERSION
from src.data.anki.anki_card import AnkiCard


@dataclass
class AnkiConnectRequestAddNotes:
    action: str = 'addNotes'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, anki_cards: List[AnkiCard]):
        self.params = {
            'notes': [
                card.to_anki_connect_params_format() for card in anki_cards
            ]
        }


@dataclass(frozen=True)
class AnkiConnectResponseAddNotes:
    result: List[bool]
    error: int
