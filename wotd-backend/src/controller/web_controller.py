import os
from typing import List

from dictcc import Dict
from singleton_decorator import singleton

from src.data.anki.anki_login_request import AnkiLoginRequest
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.dict_input.dict_options_item import DictOptionsItem, from_translation_tuples
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.language_uuid import Language
from src.data.error.database_error import DatabaseError
from src.service.anki_connect.anki_connect_fetcher import AnkiConnectFetcher
from src.service.anki_connect.vnc_service import VncService
from src.service.dict_translation.dict_translation_service import DictTranslationService
from src.service.serialization.persistence_service import PersistenceService
from src.utils.logging_config import app_log
from src.utils.translations_utils import update_request_status, update_deckname


def health_check_wrapper():
    app_log.debug('triggering health check')
    status = {
        'db_connection': PersistenceService().db_connection_is_established(),
        'anki_api_connection': AnkiConnectFetcher.health_check(),
        'wotd_api_connection': True,
    }
    app_log.debug(f"health: {status}")
    return status


@singleton
class WebController:

    def __init__(self):
        self.dictcc_translator = Dict()
        self._persistence_service = PersistenceService()
        self._available_languages: List[Language] = self._persistence_service.get_available_languages()
        self._dict_translator: DictTranslationService = DictTranslationService(self._available_languages)

    def login(self, anki_login_request: AnkiLoginRequest) -> str:
        vnc_service = VncService()
        uuid = vnc_service.login(
            username=anki_login_request.username,
            password=anki_login_request.password
        )
        # check if no decks present - need to init with some cards in order to be able to sync later on
        decknames = AnkiConnectFetcher.get_all_deck_names()
        if len(decknames) == 1 and decknames[0] == 'Default':
            vnc_service.confirm_sync()
            AnkiConnectFetcher.create_init_sync()
            vnc_service.confirm_collection_upload()

        return uuid

    def dict_available_languages_cached(self):
        if os.environ.get('PERSISTENCE_CACHE_LANGUAGES', True) \
                and len(self._available_languages) > 0:
            return self._available_languages

        self._available_languages = self._persistence_service.get_available_languages()
        return self._available_languages

    def autocomplete_dict_word(self, dict_request: DictRequest) -> List[str]:
        autocomplete_options: List[str] = self._dict_translator.autocomplete(
            prefix=dict_request.input,
            language_uuid=dict_request.from_language_uuid
        )
        app_log.debug(f'autocomplete options: {autocomplete_options} for request {dict_request}')
        return autocomplete_options

    def lookup_dict_word(self, dict_request: DictRequest,
                         auth_headers: UnsignedAuthHeaders | None) -> List[DictOptionsItem]:
        dict_request = self._persistence_service.insert_dict_request(dict_request, auth_headers)
        response_tuples = self.dictcc_translator.translate(
            word=dict_request.input,
            from_language=dict_request.from_language_uuid,
            to_language=dict_request.to_language_uuid
        ).translation_tuples
        options: List[DictOptionsItem] = from_translation_tuples(response_tuples, auth_headers)
        app_log.debug(f'lookup options: {options}')

        if auth_headers is None:
            app_log.debug(
                'user not logged into their anki web account -> webapp does not '
                'persist options, still need to generate the ids since frontend '
                'expects them')
            # generate dummy ids
            for index, item in enumerate(options):
                item.dict_options_item_id = index
            return options
        else:
            self._persistence_service.insert_single_auth_headers(auth_headers)

        update_request_status(
            original_input=dict_request.input,
            options=options
        )
        update_deckname(options, dict_request)
        app_log.debug(f'updated options: {options}')

        try:
            updated_options = self._persistence_service.insert_dict_options(options)
            app_log.debug(f'persisted dict options: {updated_options}')
            return updated_options
        except (AttributeError, DatabaseError) as e:
            app_log.error(f'database error: {e}')
            self._persistence_service.invalidate_dict_options(options)
            app_log.debug(f'not persisted dict options: {options}')
            return options

    def select_dict_word(self, item_id: int) -> bool:
        app_log.debug(f"toggle item id: {item_id}")
        self._persistence_service.update_item_select(item_id)
        return True

    def get_request_log(self) -> List[DictRequest]:
        return self._persistence_service.get_all_dict_requests()

    def anki_user_logged_in(self, auth_headers: UnsignedAuthHeaders | None) -> bool:
        return auth_headers is not None \
            and auth_headers.uuid is not None \
            and AnkiConnectFetcher.check_if_profile_present(auth_headers.uuid)
