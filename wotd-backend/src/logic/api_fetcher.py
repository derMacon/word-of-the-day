from src.data.anki.anki_card import AnkiCard
from src.utils.logging_config import app_log


class ApiFetcher:

    def __init__(self):
        pass

    def push_card(self, anki_card: AnkiCard):
        app_log.debug(f'anki card: {str(anki_card)}')
        pass

api_fetcher = ApiFetcher()