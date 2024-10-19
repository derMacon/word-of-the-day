from dataclasses import dataclass

from src.data.anki import ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectRequestGuiDeckBrowser:
    action: str = 'guiDeckBrowser'
    version: int = ANKI_CONNECT_VERSION


@dataclass(frozen=True)
class AnkiConnectResponseGuiDeckBrowser:
    result: str
    error: str
