from dataclasses import dataclass
from typing import List, Dict

from src.data.anki import ANKI_CONNECT_VERSION
from src.data.anki.anki_card import AnkiCard


@dataclass
class AnkiConnectRequestFindCards:
    action: str = 'findCards'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, anki_card: AnkiCard):
        self.params = {
            'query': f'deck:"{anki_card.deck}" front:"{anki_card.front}"'
        }


@dataclass(frozen=True)
class AnkiConnectResponseFindCards:
    result: List[bool]
    error: int
