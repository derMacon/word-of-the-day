from dataclasses import dataclass


@dataclass
class AnkiCard:
    deck: str
    front: str
    back: str

    def to_anki_connect_params_format(self):
        """
        src: https://foosoft.net/projects/anki-connect/
        """
        return {
            "deckName": self.deck,
            "modelName": "Basic",
            "fields": {
                "Front": self.front,
                "Back": self.back
            }
        }
