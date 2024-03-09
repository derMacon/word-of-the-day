from enum import Enum
from collections import namedtuple

TokenInfo = namedtuple('TokenInfo', ['name', 'id'])

class TokenType(Enum):
    MAINTOKEN = TokenInfo('main_token', 1)
    CARDTOKEN = TokenInfo('card_token', 2)

# Accessing values
print(TokenType.MAINTOKEN.value.name)  # 'main_token'
print(TokenType.MAINTOKEN.value.id)    # 1
