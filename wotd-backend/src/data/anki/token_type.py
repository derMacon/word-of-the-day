from collections import namedtuple
from enum import Enum

from src.data.anki.anki_web_endpoints import AnkiWebEndpoints

ValueInfo = namedtuple('ValueInfo', ['header_key', 'db_table', 'cookie_endpoint'])


# TODO, why do we need a db_table attribute / is this even used?
class HeaderType(Enum):
    MAIN = ValueInfo(
        header_key='Main-token',
        db_table='MAIN_TOKEN',
        cookie_endpoint=AnkiWebEndpoints.DECKS
    )
    CARD = ValueInfo(
        header_key='Card-token',
        db_table='CARD_TOKEN',
        cookie_endpoint=AnkiWebEndpoints.ADD
    )
    USER = ValueInfo(
        header_key='Anki-Email',
        db_table='USER',
        cookie_endpoint=AnkiWebEndpoints.ALL
    )
