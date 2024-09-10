from dataclasses import dataclass
from typing import List

from src.data.error.logic_error import LogicError

MERGING_SEPERATOR = ' | '


@dataclass
class AnkiCard:
    # can have multiple elem ids since multiple selectable options can be merged together before push to api
    item_ids: List[int]
    deck: str
    front: str
    back: set[str]

    def __init__(self, item_ids: List[int], deck: str, front: str, back: str):
        self.item_ids = item_ids
        self.deck = deck
        self.front = front
        self.back = {back}

    def to_anki_connect_params_format(self):
        """
        src: https://foosoft.net/projects/anki-connect/
        """
        return {
            "deckName": self.deck,
            "modelName": "Basic",
            "fields": {
                "Front": self.front,
                "Back": MERGING_SEPERATOR.join(self.back)
            }
        }

    def merge_cards(self, other_cards) -> 'AnkiCard':
        if other_cards is None:
            raise LogicError(f'anki card merge error - cannot merge null pointer')

        if len(other_cards) == 0:
            return self

        other_cards_decks = list(set([card.deck for card in other_cards]))
        if len(other_cards_decks) > 1 or other_cards_decks[0] != self.deck:
            raise LogicError(f'cannot merge other cards since decks do not match. '
                             f'self deck {self.deck} vs. other decks {other_cards_decks}')

        other_cards_fronts = list(set([card.front for card in other_cards]))
        if len(other_cards_fronts) == 0 or len(other_cards_fronts) > 1 or other_cards_fronts[0] != self.front:
            raise LogicError(f'cannot merge other cards since fronts do not match. '
                             f'self deck {self.front} vs. other decks {other_cards_fronts}')

        for card in other_cards:
            self.item_ids.extend(card.item_ids)
            self.back.update(card.back)

        return self
