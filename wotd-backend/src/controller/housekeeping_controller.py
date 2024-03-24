import os
import threading
from time import sleep
from typing import List

from src.data.anki.anki_card import AnkiCard
from src.data.dict_input.anki_login_response_headers import AnkiLoginResponseHeaders
from src.data.dict_input.status import Status
from src.data.error.database_error import DatabaseError
from src.service.anki_api_fetcher import anki_api_fetcher
from src.service.persistence_service import PersistenceService
from src.utils.logging_config import app_log

MAX_CONNECTION_TRIES = 3


def trigger_housekeeping(auth_headers: AnkiLoginResponseHeaders):
    delay_sec = float(os.environ['HOUSEKEEPING_INTERVAL_SEC'])  # TODO dont hardcode this
    threading.Timer(delay_sec, sync_anki_push, args=(delay_sec, auth_headers,)).start()


def sync_anki_push(housekeeping_interval, auth_headers: AnkiLoginResponseHeaders):
    try:
        app_log.debug(f'sync anki push with interval: {housekeeping_interval}')

        error_cnt = 0
        while not PersistenceService().db_connection_is_established() and error_cnt < MAX_CONNECTION_TRIES:
            error_cnt = error_cnt + 1
            sleep(housekeeping_interval)

        if PersistenceService().db_connection_is_established() and anki_api_fetcher.health_check():
            _push_data(housekeeping_interval, auth_headers)
        else:
            app_log.debug('not possible to push data to anki api - try pushing with next cleanup job')

    except DatabaseError as e:
        app_log.error(f"error: '{e}'")


def _push_data(housekeeping_interval, auth_headers: AnkiLoginResponseHeaders):
    persisted_options = PersistenceService().find_expired_options(housekeeping_interval)
    ids_to_delete: List[int] = []
    for curr_option in persisted_options:

        if curr_option.status == Status.OK and curr_option.selected:
            app_log.debug(f"selected option with id '{curr_option.dict_options_item_id}' "
                          f"with status {curr_option.status}")

            card_input = AnkiCard(
                deck=curr_option.deck,
                front=curr_option.input,
                back=curr_option.output,
            )

            response_ok = anki_api_fetcher.api_push_card(card_input, auth_headers)
            if response_ok:
                PersistenceService().update_item_status(curr_option.dict_options_item_id, Status.SYNCED)
            else:
                app_log.error(f"not able to push card '{str(card_input)}'")

        elif curr_option.status != Status.SYNCED:
            ids_to_delete.append(curr_option.dict_options_item_id)

    app_log.debug(f'id_to_delete: {ids_to_delete}')
    PersistenceService().delete_items_with_ids(ids_to_delete)