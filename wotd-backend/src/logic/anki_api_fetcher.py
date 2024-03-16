from dataclasses import asdict

import requests

from src.data.anki.anki_card import AnkiCard
from src.data.anki.token_type import TokenType
from src.utils.logging_config import app_log


class AnkiApiFetcher:

    # TODO use .ini file
    ANKI_API_SERVER_ADDRESS = 'http://192.168.178.187:4000'
    ANKI_API_BASE = 'http://192.168.178.187:4000/api/v1'

    def login(self, username: str, password: str):
        app_log.debug(f"user '{username}' tries to login")

        url = self.ANKI_API_BASE + '/login'

        data = {
            'username': username,
            'password': password
        }

        headers = {
            'Content-Type': 'application/json',  # Example header
            # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Example header for authorization
        }

        # Sending the POST request
        response = requests.post(url, json=data, headers=headers)

        # TODO decorator similar to sql error - here for the api communication
        # if response.status_code == 200:
        #     print("POST request was successful.")
        #     print("Response:", response.headers)
        # else:
        #     print("POST request failed with status code:", response.status_code)
        
        return (response.headers[TokenType.MAIN.value.header_key],
                response.headers[TokenType.CARD.value.header_key])

    def push_card(self, anki_card: AnkiCard, headers):
        app_log.debug(f'anki card: {str(anki_card)}')
        url = self.ANKI_API_BASE + '/add-card'
        data = asdict(anki_card)
        requests.get(url, json=data, headers=headers)


anki_api_fetcher = AnkiApiFetcher()
