from dataclasses import dataclass
from typing import List, Dict

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass
class AnkiConnectRequestLoadProfile:
    action: str = 'loadProfile'
    version: int = ANKI_CONNECT_VERSION
    params: Dict[str, str] = None

    def __init__(self, name: str):
        self.params = {
            'name': name
        }


@dataclass(frozen=True)
class AnkiConnectResponseLoadProfile:
    result: List[str]
    error: str
