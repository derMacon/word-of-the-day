from dataclasses import dataclass
from typing import List, Dict

from src.data.anki import ANKI_CONNECT_VERSION
from src.data.anki.anki_card import AnkiCard


@dataclass(frozen=True)
class AnkiConnectRequestCanAddNotes:
    action: str = 'canAddNotes'
    version: int = ANKI_CONNECT_VERSION
    params: List[Dict[str, str]]

    def __init__(self, anki_cards: List[AnkiCard]):
        # TODO
        pass


@dataclass(frozen=True)
class AnkiConnectResponseCanAddNotes:
    result: List[bool]
    error: int
