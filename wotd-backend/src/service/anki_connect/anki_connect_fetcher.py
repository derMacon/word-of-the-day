import dataclasses
import os
from typing import List

import requests

from src.data.anki.anki_card import AnkiCard
from src.data.anki.anki_connect_add_notes import AnkiConnectRequestAddNotes, AnkiConnectResponseAddNotes
from src.data.anki.anki_connect_can_add_notes import AnkiConnectRequestCanAddNotes, AnkiConnectResponseCanAddNotes
from src.data.anki.anki_connect_card_info import AnkiConnectRequestCardsInfo, AnkiConnectResponseCardsInfo
from src.data.anki.anki_connect_create_deck import AnkiConnectRequestCreateDeck, AnkiConnectResponseCreateDeck
from src.data.anki.anki_connect_delete_notes import AnkiConnectRequestDeleteNotes, AnkiConnectResponseDeleteNotes
from src.data.anki.anki_connect_find_cards import AnkiConnectRequestFindCards, AnkiConnectResponseFindCards
from src.data.anki.anki_connect_get_deck_names import AnkiConnectRequestGetDeckNames, AnkiConnectResponseGetDeckNames
from src.data.anki.anki_connect_get_profiles import AnkiConnectRequestGetProfiles, AnkiConnectResponseGetProfiles
from src.data.anki.anki_connect_gui_deck_browser import AnkiConnectRequestGuiDeckBrowser, \
    AnkiConnectResponseGuiDeckBrowser
from src.data.anki.anki_connect_load_profile import AnkiConnectRequestLoadProfile
from src.data.anki.anki_connect_notes_info import AnkiConnectRequestNotesInfo, AnkiConnectResponseNotesInfo
from src.data.anki.anki_connect_sync import AnkiConnectRequestSync, AnkiConnectResponseSync
from src.data.dict_input import now
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.dict_input.env_collection import ConnectionEnv
from src.data.error.anki_connect_error import AnkiConnectError
from src.utils.logging_config import app_log


class AnkiConnectFetcher:
    ANKI_CONNECT_HOST = os.environ.get(ConnectionEnv.ENV_ANKI_CONNECT_HOST, 'localhost')
    ANKI_CONNECT_DATA_PORT = os.environ.get(ConnectionEnv.ENV_ANKI_CONNECT_DATA_PORT, 8765)
    ANKI_CONNECT_LOGIN_PORT = os.environ.get(ConnectionEnv.ENV_ANKI_CONNECT_LOGIN_PORT, 5900)

    ANKI_CONNECT_DATA_ADDRESS = f'http://{ANKI_CONNECT_HOST}:{ANKI_CONNECT_DATA_PORT}'

    @staticmethod
    def health_check():
        app_log.debug(f"anki connect triggering health check at - '{AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS}'")
        try:

            data = dataclasses.asdict(AnkiConnectRequestGetDeckNames())
            plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
            anki_connect_response: AnkiConnectResponseGetDeckNames = AnkiConnectResponseGetDeckNames(**plain_response)
            app_log.debug(f'anki connect response for get deck names: {anki_connect_response}')

            return anki_connect_response.error is None
        except Exception as e:
            app_log.error(e)
            return False

    @staticmethod
    def api_push_cards(anki_cards: List[AnkiCard], headers: UnsignedAuthHeaders) -> AnkiConnectResponseAddNotes:
        app_log.debug(f'auth headers: {headers}')
        app_log.debug(f'push anki card: {anki_cards}')

        profile_uuid = headers.uuid
        AnkiConnectFetcher._validate_if_profile_present(profile_uuid)
        AnkiConnectFetcher.load_profile(profile_uuid)
        AnkiConnectFetcher.sync_anki_web()
        AnkiConnectFetcher._create_decks_if_needed(anki_cards)

        push_response: AnkiConnectResponseAddNotes = AnkiConnectFetcher._add_notes(anki_cards)
        AnkiConnectFetcher.sync_anki_web()

        return push_response

    @staticmethod
    def _validate_if_profile_present(profile_uuid: str) -> None:
        if not AnkiConnectFetcher.check_if_profile_present(profile_uuid):
            raise AnkiConnectError(f'user profile not created before pushing: {profile_uuid}')
        app_log.debug(f"profile uuid '{profile_uuid}' present in available profiles")

    @staticmethod
    def check_if_profile_present(profile_uuid: str) -> bool:
        app_log.debug(f'checking if profile uuid is present in anki stack: {profile_uuid}')
        if profile_uuid is None:
            app_log.debug('profile uuid was None - invalid uuid to look up')
            return False

        data = dataclasses.asdict(AnkiConnectRequestGetProfiles())
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetProfiles = AnkiConnectResponseGetProfiles(**plain_response)
        app_log.debug(f'anki connect response for get profiles (curr profile {profile_uuid}): {anki_connect_response}')
        uuid_is_present = profile_uuid in anki_connect_response.result
        app_log.debug(f'profile uuid is present: {uuid_is_present}')
        return uuid_is_present

    @staticmethod
    def load_profile(profile_uuid: str) -> None:
        app_log.debug(f"loading profile uuid '{profile_uuid}'")
        data = dataclasses.asdict(AnkiConnectRequestLoadProfile(name=profile_uuid))
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetProfiles = AnkiConnectResponseGetProfiles(**plain_response)
        app_log.debug(f'anki connect response for load profile: {anki_connect_response}')
        app_log.debug(f'profile load successful: '
                      f'{anki_connect_response is not None and anki_connect_response.error is None}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'unable to load profile {profile_uuid} :: {anki_connect_response}')

    @staticmethod
    def _create_decks_if_needed(anki_cards: List[AnkiCard]) -> None:
        unique_decks = set([card.deck for card in anki_cards])
        app_log.debug(f"create decks if needed, unique decks: '{unique_decks}'")

        for deck_name in unique_decks:
            if not AnkiConnectFetcher.check_if_deck_is_present(deck_name):
                AnkiConnectFetcher._create_single_deck(deck_name)

    @staticmethod
    def check_if_deck_is_present(deck_name: str) -> bool:
        return deck_name in AnkiConnectFetcher.get_all_deck_names()

    @staticmethod
    def get_all_deck_names() -> List[str]:
        data = dataclasses.asdict(AnkiConnectRequestGetDeckNames())
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGetDeckNames = AnkiConnectResponseGetDeckNames(**plain_response)
        app_log.debug(f'anki connect response for get deck names: {anki_connect_response}')

        if (anki_connect_response is None
                or anki_connect_response.result is None
                or anki_connect_response.error is not None):
            raise AnkiConnectError(f'unable to retrieve deck names from api :: {anki_connect_response}')

        return anki_connect_response.result

    @staticmethod
    def _create_single_deck(deck_name: str) -> None:
        app_log.debug(f'trying to create deck with name: {deck_name}')
        data = dataclasses.asdict(AnkiConnectRequestCreateDeck(deck_name))
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseCreateDeck = AnkiConnectResponseCreateDeck(**plain_response)
        app_log.debug(f'anki connect response for create deck: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'unable to create deck {deck_name} :: {anki_connect_response}')

    @staticmethod
    def _cards_can_be_added(anki_cards: List[AnkiCard]) -> List[bool]:
        data = dataclasses.asdict(AnkiConnectRequestCanAddNotes(anki_cards))
        app_log.debug(f'anki connect can add notes request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseCanAddNotes = AnkiConnectResponseCanAddNotes(**plain_response)
        app_log.debug(f'anki connect response for can add notes: {anki_connect_response}')

        if anki_connect_response is not None and all(anki_connect_response.result):
            app_log.debug('all anki cards valid, can be added to vault')
        else:
            app_log.error(f'cannot add all anki cards'
                          f' - AnkiConnectResponseCanAddNotes output: {anki_connect_response} '
                          f':: anki_cards: {anki_cards}')

        return anki_connect_response.result

    @staticmethod
    def _find_pushed_anki_id(anki_card: AnkiCard) -> int:
        data = dataclasses.asdict(AnkiConnectRequestFindCards(anki_card))
        app_log.debug(f'anki connect find cards request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseFindCards = AnkiConnectResponseFindCards(**plain_response)
        app_log.debug(f'anki connect response for find cards: {anki_connect_response}')

        if anki_connect_response is None \
                or anki_connect_response.error is not None \
                or anki_connect_response.result is None \
                or len(anki_connect_response.result) == 0:
            raise AnkiConnectError(f'could not find cards for {anki_connect_response} '
                                   f':: invalid card: {anki_card}')

        return anki_connect_response.result[0]

    @staticmethod
    def _delete_cards(duplicate_cards: List[AnkiCard]) -> None:
        unique_ids_to_delete = list(set([curr_card.anki_id for curr_card in duplicate_cards]))
        data = dataclasses.asdict(AnkiConnectRequestDeleteNotes(unique_ids_to_delete))
        app_log.debug(f'anki connect delete notes request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseDeleteNotes = AnkiConnectResponseDeleteNotes(**plain_response)
        app_log.debug(f'anki connect response for delete notes: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'could not delete notes for {anki_connect_response} '
                                   f':: duplicate cards: {duplicate_cards}')

    @staticmethod
    def _get_card_by_id(anki_card_id: int) -> AnkiCard:
        data = dataclasses.asdict(AnkiConnectRequestCardsInfo(anki_card_id))
        app_log.debug(f'anki connect cards info request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseCardsInfo = AnkiConnectResponseCardsInfo(**plain_response)
        app_log.debug(f'anki connect response for cards info: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'could get card info from anki api {anki_connect_response} '
                                   f':: invalid card id: {anki_card_id}')

        result_map = anki_connect_response.result[0]
        return AnkiCard(
            anki_id=result_map['note'],
            deck=result_map['deckName'],
            front=result_map['fields']['Front']['value'],
            back=result_map['fields']['Back']['value'],
            ts=now()
        )

    @staticmethod
    def _get_card_id_by_note_id(anki_card_id: int) -> int:
        data = dataclasses.asdict(AnkiConnectRequestNotesInfo(anki_card_id))
        app_log.debug(f'anki connect notes info request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseNotesInfo = AnkiConnectResponseNotesInfo(**plain_response)
        app_log.debug(f'anki connect response for notes info: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'could get notes info from anki api {anki_connect_response} '
                                   f':: invalid notes id: {anki_card_id}')
        try:
            return anki_connect_response.result[0]['cards'][0]
        except:
            raise AnkiConnectError(
                f'trouble unwrapping anki response for notes info request, response: {anki_connect_response} '
                f':: invalid notes id: {anki_card_id}')

    @staticmethod
    def _add_notes(anki_cards: List[AnkiCard]) -> AnkiConnectResponseAddNotes:
        data = dataclasses.asdict(AnkiConnectRequestAddNotes(anki_cards))
        app_log.debug(f'anki connect add notes request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseAddNotes = AnkiConnectResponseAddNotes(**plain_response)
        app_log.debug(f'anki connect response for add notes: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            raise AnkiConnectError(f'could not push cards to anki api {anki_connect_response} '
                                   f':: invalid cards: {anki_cards}')

        return anki_connect_response

    @staticmethod
    def sync_anki_web() -> None:
        app_log.debug('trigger sync with anki web')
        data = dataclasses.asdict(AnkiConnectRequestSync())
        app_log.debug(f'anki connect sync request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseSync = AnkiConnectResponseSync(**plain_response)
        app_log.debug(f'anki connect response for sync: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            app_log.error(f'could not sync with anki web: {anki_connect_response}')

    @staticmethod
    def create_init_sync() -> None:
        app_log.debug('create initial sync')
        deck = 'wotd'  # TODO use constant
        AnkiConnectFetcher._create_single_deck(deck)
        anki_cards: AnkiCard = AnkiCard(
            deck=deck,
            front='version',
            back=os.getenv('WOTD_VERSION', '1.0.0'),
            ts=now(),
        )

        AnkiConnectFetcher._create_decks_if_needed([anki_cards])
        AnkiConnectFetcher._add_notes([anki_cards])
        AnkiConnectFetcher.sync_anki_web()

    @staticmethod
    def reload_gui_deck_view() -> None:
        app_log.debug('reloading gui deck view')
        data = dataclasses.asdict(AnkiConnectRequestGuiDeckBrowser())
        app_log.debug(f'anki connect gui deck browser request json: {data}')
        plain_response = requests.post(url=AnkiConnectFetcher.ANKI_CONNECT_DATA_ADDRESS, json=data).json()
        anki_connect_response: AnkiConnectResponseGuiDeckBrowser = AnkiConnectResponseGuiDeckBrowser(**plain_response)
        app_log.debug(f'anki connect response for gui deck browser: {anki_connect_response}')

        if anki_connect_response is None or anki_connect_response.error is not None:
            app_log.error(f'could not execute gui deck browser with anki web: {anki_connect_response}')


