from enum import Enum
from collections import namedtuple

# TokenInfo = namedtuple('TokenInfo', ['name', 'id'])

class TokenType(Enum):
    MAINTOKEN = 'main_token'
    CARDTOKEN = 'card_token'
