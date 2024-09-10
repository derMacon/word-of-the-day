from dataclasses import dataclass
from typing import List

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectRequestSync:
    action: str = 'sync'
    version: int = ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectResponseSync:
    result: str
    error: int
