from dataclasses import dataclass

from src.data.anki.token_type import HeaderType


# TODO delete this - it not used
@dataclass
class AnkiLoginResponseHeaders:
    username: str
    main_token: str
    card_token: str

    def to_map(self):
        return {
            HeaderType.USER.value.header_key: self.username,
            HeaderType.MAIN.value.header_key: self.main_token,
            HeaderType.CARD.value.header_key: self.card_token
        }
