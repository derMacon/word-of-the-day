from enum import Enum


class TokenType(str, Enum):
    MAINTOKEN = 'main_token'
    CARDTOKEN = 'card_token'
