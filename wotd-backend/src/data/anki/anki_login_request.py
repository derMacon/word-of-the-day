from dataclasses import dataclass


@dataclass
class AnkiLoginRequest:
    username: str
    password: str
