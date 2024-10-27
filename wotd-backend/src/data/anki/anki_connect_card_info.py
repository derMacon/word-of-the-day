from dataclasses import dataclass
from typing import Dict

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass
class AnkiConnectRequestCardsInfo:
    action: str = 'cardsInfo'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, anki_card_id: int):
        self.params = {
            'cards': [anki_card_id]
        }


@dataclass(frozen=True)
class AnkiConnectResponseCardsInfo:
    result: str
    error: str
