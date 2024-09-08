import dataclasses
import os
from typing import List

import requests

from src.data.anki.anki_card import AnkiCard
from src.data.anki.anki_connect_get_deck_names import AnkiConnectRequestGetDeckNames, AnkiConnectResponseGetDeckNames
from src.data.anki.anki_connect_get_profiles import AnkiConnectRequestGetProfiles, AnkiConnectResponseGetProfiles
from src.data.anki.anki_connect_load_profile import AnkiConnectRequestLoadProfile
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.utils.logging_config import app_log


class WotdAnkiConnectFetcher:
    ANKI_CONNECT_HOST = os.environ.get('ANKI_CONNECT_HOST', 'localhost')
    ANKI_CONNECT_DATA_PORT = os.environ.get('ANKI_CONNECT_DATA_PORT', 8765)
    ANKI_CONNECT_LOGIN_PORT = os.environ.get('ANKI_CONNECT_LOGIN_PORT', 5900)

    ANKI_CONNECT_DATA_ADDRESS = f'http://{ANKI_CONNECT_HOST}:{ANKI_CONNECT_DATA_PORT}'

    @staticmethod
    def health_check():
        app_log.debug('anki connect triggering health check')
        try:

            data = dataclasses.asdict(AnkiConnectRequestGetDeckNames())
            plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
            anki_connect_response: AnkiConnectResponseGetDeckNames = AnkiConnectResponseGetDeckNames(**plain_response)
            app_log.debug(f'anki connect response for get deck names: {anki_connect_response}')

            return anki_connect_response.error is None
        except Exception as e:
            app_log.error(e)
            return False

    @staticmethod
    def api_push_card(self, anki_card: AnkiCard, headers: UnsignedAuthHeaders) -> bool:
        # app_log.debug(f'push anki card: {str(anki_card)}')
        # url = self.ANKI_API_BASE + '/add-card'
        # data = asdict(anki_card)
        # app_log.debug(f"push data '{data}' to url '{url}' with headers '{headers}'")
        # return requests.get(url, json=data, headers=headers.to_map()).ok

        app_log.debug(f'auth headers: {headers}')
        app_log.debug(f'push anki card: {str(anki_card)}')

        # profile_uuid = headers.uuid
        # WotdAnkiConnectFetcher._validate_if_profile_present(profile_uuid)
        # WotdAnkiConnectFetcher._load_profile(profile_uuid)

    @staticmethod
    def _validate_if_profile_present(profile_uuid: str) -> None:
        data = dataclasses.asdict(AnkiConnectRequestGetProfiles())
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetProfiles = AnkiConnectResponseGetProfiles(**plain_response)
        app_log.debug(f'anki connect response for get profiles: {anki_connect_response}')
        if profile_uuid not in anki_connect_response.result:
            # TODO throw dedicated error (test this and react appropriately)
            pass

    @staticmethod
    def _load_profile(profile_uuid: str) -> None:
        data = dataclasses.asdict(AnkiConnectRequestLoadProfile(name=profile_uuid))
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetProfiles = AnkiConnectResponseGetProfiles(**plain_response)
        app_log.debug(f'anki connect response for load profile: {anki_connect_response}')

    @staticmethod
    def _validate_notes_can_be_added(anki_cards: List[AnkiCard]) -> bool:
        data = dataclasses.asdict(AnkiConnectRequestGetProfiles())
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetProfiles = AnkiConnectResponseGetProfiles(**plain_response)
        app_log.debug(f'anki connect response for get profiles: {anki_connect_response}')
        return profile_uuid in anki_connect_response.result
