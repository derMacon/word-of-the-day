from src.data.anki.anki_card import AnkiCard
from src.utils.logging_config import app_log


class AnkiApiFetcher:

    def __init__(self):
        pass

    def login(self, username: str, password: str):
        app_log.debug(f"user '{username}' tries to login")
        return 'testheader1', 'testheader2'

    def push_card(self, anki_card: AnkiCard):
        app_log.debug(f'anki card: {str(anki_card)}')
        pass


anki_api_fetcher = AnkiApiFetcher()
