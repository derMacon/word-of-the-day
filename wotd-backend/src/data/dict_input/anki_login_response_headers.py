from dataclasses import dataclass

from src.data.anki.token_type import TokenType


# TODO delete this - it not used
@dataclass
class AnkiLoginResponseHeaders:
    main_token: str
    card_token: str

    def to_map(self):
        return {
            TokenType.MAIN.value.header_key: self.main_token,
            TokenType.CARD.value.header_key: self.card_token
        }
