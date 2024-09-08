from dataclasses import dataclass
from typing import List

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectRequestGetProfiles:
    action: str = 'getProfiles'
    version: int = ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectResponseGetProfiles:
    result: List[str]
    error: int
