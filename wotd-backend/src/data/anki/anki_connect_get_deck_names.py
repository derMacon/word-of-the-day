from dataclasses import dataclass
from typing import List, Dict

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectRequestGetDeckNames:
    action: str = 'deckNames'
    version: int = ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectResponseGetDeckNames:
    result: List[str]
    error: str
