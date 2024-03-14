from dataclasses import dataclass

@dataclass
class AnkiCard:
    deck: str
    front: str
    back: str

    # def __init__(self, deck: str, front: str, back: str):
    #     self.deck = deck
    #     self.front = front
    #     self.back = back
