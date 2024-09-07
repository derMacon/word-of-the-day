import os
from dataclasses import asdict

import requests

from src.data.anki.anki_card import AnkiCard
from src.data.anki.anki_connect_response_wrapper import AnkiConnectResponseWrapper
from src.data.anki.token_type import HeaderType
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.utils.logging_config import app_log


# TODO make functions static or use singleton decorator - only works without constants in the class (first put them into .ini file)
class WotdApiFetcher:
    ANKI_CONNECT_HOST = os.environ.get('ANKI_CONNECT_HOST', 'localhost')
    ANKI_CONNECT_DATA_PORT = os.environ.get('ANKI_CONNECT_DATA_PORT', 8765)
    ANKI_CONNECT_LOGIN_PORT = os.environ.get('ANKI_CONNECT_LOGIN_PORT', 5900)

    ANKI_CONNECT_DATA_ADDRESS_POST = f'http://{ANKI_CONNECT_HOST}:{ANKI_CONNECT_DATA_PORT}'
    ANKI_CONNECT_LOGIN_ADDRESS_VNC = f'{ANKI_CONNECT_HOST}::{ANKI_CONNECT_LOGIN_PORT}'

    def health_check(self):
        try:
            data = {
                "action": "deckNames",
                "version": 6
            }

            app_log.debug('triggering health check for anki connect api container')
            plain_response = requests.post(url=WotdApiFetcher.ANKI_CONNECT_DATA_ADDRESS_POST, json=data).json()
            anki_connect_response = AnkiConnectResponseWrapper(**plain_response)
            app_log.debug(f'anki_connect_response: {anki_connect_response.error}')

            return anki_connect_response.error is None
        except Exception as e:
            app_log.error(e)
            return False

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

        main_token = response.headers[HeaderType.MAIN.value.header_key]
        card_token = response.headers[HeaderType.CARD.value.header_key]

        app_log.debug(f"main token: '{main_token}'")
        app_log.debug(f"card token: '{card_token}'")

        return main_token, card_token

    def api_push_card(self, anki_card: AnkiCard, headers: UnsignedAuthHeaders) -> bool:
        app_log.debug(f'push anki card: {str(anki_card)}')
        url = self.ANKI_API_BASE + '/add-card'
        data = asdict(anki_card)
        app_log.debug(f"push data '{data}' to url '{url}' with headers '{headers}'")
        return requests.get(url, json=data, headers=headers.to_map()).ok


anki_api_fetcher = WotdApiFetcher()
