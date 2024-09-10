import dataclasses
import os
from typing import List

import requests

from src.data.anki.anki_card import AnkiCard
from src.data.anki.anki_connect_add_notes import AnkiConnectRequestAddNotes, AnkiConnectResponseAddNotes
from src.data.anki.anki_connect_can_add_notes import AnkiConnectRequestCanAddNotes, AnkiConnectResponseCanAddNotes
from src.data.anki.anki_connect_get_deck_names import AnkiConnectRequestGetDeckNames, AnkiConnectResponseGetDeckNames
from src.data.anki.anki_connect_get_profiles import AnkiConnectRequestGetProfiles, AnkiConnectResponseGetProfiles
from src.data.anki.anki_connect_load_profile import AnkiConnectRequestLoadProfile
from src.data.anki.anki_connect_sync import AnkiConnectRequestSync, AnkiConnectResponseSync
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.error.anki_connect_error import AnkiConnectError
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
    def api_push_cards(anki_cards: List[AnkiCard], headers: UnsignedAuthHeaders) -> bool:
        # app_log.debug(f'push anki card: {str(anki_card)}')
        # url = self.ANKI_API_BASE + '/add-card'
        # data = asdict(anki_card)
        # app_log.debug(f"push data '{data}' to url '{url}' with headers '{headers}'")
        # return requests.get(url, json=data, headers=headers.to_map()).ok

        app_log.debug(f'auth headers: {headers}')
        app_log.debug(f'push anki card: {anki_cards}')

        profile_uuid = headers.uuid
        WotdAnkiConnectFetcher._validate_if_profile_present(profile_uuid)
        WotdAnkiConnectFetcher._load_profile(profile_uuid)
        WotdAnkiConnectFetcher._validate_notes_can_be_added(anki_cards)
        WotdAnkiConnectFetcher._add_notes(anki_cards)
        WotdAnkiConnectFetcher._sync_anki_web()
        return True

    @staticmethod
    def _validate_if_profile_present(profile_uuid: str) -> None:
        if not WotdAnkiConnectFetcher.check_if_profile_present(profile_uuid):
            raise AnkiConnectError(f'user profile not created before pushing: {profile_uuid}')
        app_log.debug(f"profile uuid '{profile_uuid}' present in available profiles")

    @staticmethod
    def check_if_profile_present(profile_uuid: str) -> bool:
        app_log.debug(f'checking if profile uuid is present in anki stack: {profile_uuid}')
        if profile_uuid is None:
            app_log.debug('profile uuid was None - invalid uuid to look up')
            return False

        data = dataclasses.asdict(AnkiConnectRequestGetProfiles())
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetProfiles = AnkiConnectResponseGetProfiles(**plain_response)
        app_log.debug(f'anki connect response for get profiles (curr profile {profile_uuid}): {anki_connect_response}')
        uuid_is_present = profile_uuid in anki_connect_response.result
        app_log.debug(f'profile uuid is present: {uuid_is_present}')
        return uuid_is_present

    @staticmethod
    def _load_profile(profile_uuid: str) -> None:
        app_log.debug(f"loading profile uuid '{profile_uuid}'")
        data = dataclasses.asdict(AnkiConnectRequestLoadProfile(name=profile_uuid))
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetProfiles = AnkiConnectResponseGetProfiles(**plain_response)
        app_log.debug(f'anki connect response for load profile: {anki_connect_response}')
        app_log.debug(f'profile load successful: '
                      f'{anki_connect_response is not None and anki_connect_response.error is None}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'unable to load profile {profile_uuid} :: {anki_connect_response}')

    @staticmethod
    def _validate_notes_can_be_added(anki_cards: List[AnkiCard]) -> None:
        data = dataclasses.asdict(AnkiConnectRequestCanAddNotes(anki_cards))
        app_log.debug(f'anki connect can add notes request json: {data}')
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseCanAddNotes = AnkiConnectResponseCanAddNotes(**plain_response)
        app_log.debug(f'anki connect response for can add notes: {anki_connect_response}')

        if anki_connect_response is not None and all(anki_connect_response.result):
            app_log.debug('all anki cards valid, can be added to vault')
        else:
            raise AnkiConnectError(f'cannot add all anki cards'
                                        f' - AnkiConnectResponseCanAddNotes output: {anki_connect_response} '
                                        f':: anki_cards: {anki_cards}')

    @staticmethod
    def _add_notes(anki_cards: List[AnkiCard]) -> None:
        data = dataclasses.asdict(AnkiConnectRequestAddNotes(anki_cards))
        app_log.debug(f'anki connect add notes request json: {data}')
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseAddNotes = AnkiConnectResponseAddNotes(**plain_response)
        app_log.debug(f'anki connect response for add notes: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'could not push cards to anki api {anki_connect_response} '
                                   f':: invalid cards: {anki_cards}')

    @staticmethod
    def _sync_anki_web() -> None:
        app_log.log('trigger sync with anki web')
        data = dataclasses.asdict(AnkiConnectRequestSync())
        app_log.debug(f'anki connect sync request json: {data}')
        plain_response = requests.post(url=WotdAnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseSync = AnkiConnectResponseSync(**plain_response)
        app_log.debug(f'anki connect response for sync: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'could not sync with anki web: {anki_connect_response}')
