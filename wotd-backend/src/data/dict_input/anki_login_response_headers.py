from dataclasses import dataclass

from src.data.anki.token_type import HeaderType


@dataclass
class UnsignedAuthHeaders:
    username: str
    uuid: str

    def to_map(self):
        return {
            HeaderType.UNSIGNED_USERNAME: self.username,
            HeaderType.UNSIGNED_UUID: self.uuid,
        }
