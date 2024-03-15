from collections import namedtuple
from enum import Enum

from src.data.anki.anki_web_endpoints import AnkiWebEndpoints

TokenInfo = namedtuple('TokenInfo', ['header_key', 'db_table', 'cookie_endpoint'])


class TokenType(Enum):
    MAIN = TokenInfo(
        header_key='Main-token',
        db_table='MAIN_TOKEN',
        cookie_endpoint=AnkiWebEndpoints.DECKS
    )
    CARD = TokenInfo(
        header_key='Card-token',
        db_table='CARD_TOKEN',
        cookie_endpoint=AnkiWebEndpoints.ADD
    )
