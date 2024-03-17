import threading
import os
from typing import List

from dictcc import Dict

from src.data.dict_input.anki_login_response_headers import AnkiLoginResponseHeaders
from src.data.dict_input.dict_options_item import DictOptionsItem, from_translation_tuples
from src.data.dict_input.dict_request import DictRequest
from src.logic.housekeeping_controller import sync_anki_push
from src.service.persistence_service import PersistenceService
from src.utils.logging_config import app_log
from src.utils.translations_utils import update_status, update_deckname


class WebController:

    def __init__(self):
        self.dictcc_translator = Dict()
        self.persistence_service = PersistenceService()


    def lookup_dict_word(self, dict_request: DictRequest, auth_headers: AnkiLoginResponseHeaders | None) -> List[DictOptionsItem]:
        response_tuples = self.dictcc_translator.translate(
            word=dict_request.input,
            from_language=dict_request.from_language_uuid.name.lower(),
            to_language=dict_request.to_language_uuid.name.lower()
        ).translation_tuples
        options: List[DictOptionsItem] = from_translation_tuples(response_tuples)
        app_log.debug(f'lookup options: {options}')

        if auth_headers is None:
            app_log.debug('user not logged into their anki web account -> webapp does not persist options')
            return options

        update_status(
            original_input=dict_request.input,
            options=options
        )
        update_deckname(options, dict_request)
        app_log.debug(f'updated options: {options}')

        updated_options = self.persistence_service.insert_dict_options(options)
        app_log.debug(f'persisted dict options: {updated_options}')

        delay_sec = float(os.environ['HOUSEKEEPING_INTERVAL_SEC']) # TODO dont hardcode this
        threading.Timer(delay_sec, sync_anki_push, args=(delay_sec, auth_headers, )).start()

        return updated_options

    def select_dict_word(self, item_id: int) -> bool:
        app_log.debug(f"toggle item id: {item_id}")
        self.persistence_service.update_selected_item(item_id)
        return True


controller = WebController()
