from dataclasses import dataclass
from typing import List, Dict

from src.data.anki import ANKI_CONNECT_VERSION
from src.data.anki.anki_card import AnkiCard


@dataclass
class AnkiConnectRequestCreateDeck:
    action: str = 'createDeck'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, deck_name: str):
        self.params = {
            'deck': deck_name
        }


@dataclass(frozen=True)
class AnkiConnectResponseCreateDeck:
    result: int
    error: str
