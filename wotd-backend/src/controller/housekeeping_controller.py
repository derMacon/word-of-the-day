import os
import threading
from time import sleep
from typing import List, Tuple

from more_itertools import chunked

from src.data.anki.anki_card import AnkiCard
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.requeststatus import RequestStatus
from src.data.error.database_error import DatabaseError
from src.data.error.missing_headers_error import MissingHeadersError
from src.service.persistence_service import PersistenceService
from src.service.wotd_api_fetcher import WotdAnkiConnectFetcher
from src.utils.logging_config import app_log

MAX_CONNECTION_TRIES = 3
API_CONNECT_BATCH_SIZE = 10
DB_BATCH_SIZE = 100


def trigger_housekeeping(auth_headers: UnsignedAuthHeaders):
    if auth_headers is None:
        raise MissingHeadersError('missing headers when syncing anki push')

    delay_sec = float(os.environ['HOUSEKEEPING_INTERVAL_SEC'])  # TODO dont hardcode this
    app_log.debug(f'triggering housekeeping in {delay_sec} secs')
    threading.Timer(delay_sec, sync_anki_push, args=(delay_sec, auth_headers,)).start()


def sync_anki_push(housekeeping_interval, auth_headers: UnsignedAuthHeaders):
    try:
        app_log.debug(f'sync anki push with delay {housekeeping_interval} s and {auth_headers}')

        error_cnt = 0
        while not PersistenceService().db_connection_is_established() and error_cnt < MAX_CONNECTION_TRIES:
            error_cnt = error_cnt + 1
            sleep(housekeeping_interval)

        if PersistenceService().db_connection_is_established() and WotdAnkiConnectFetcher.health_check():
            _push_data(housekeeping_interval, auth_headers)
        else:
            app_log.debug('not possible to push data to anki connect api - try pushing with next cleanup job')

    except DatabaseError as e:
        app_log.error(f"error: '{e}'")


def _push_data(housekeeping_interval, auth_headers: UnsignedAuthHeaders):
    app_log.debug('preparing data to push to anki connect')
    persisted_options: List[DictOptionsItem] = PersistenceService().find_expired_options_for_user(
        housekeeping_interval,
        auth_headers
    )
    cards_to_push, ids_to_delete = _filter_elems(persisted_options)
    _push_in_batches(cards_to_push, auth_headers)
    _delete_elems_in_batches(ids_to_delete)


def _filter_elems(persisted_options: List[DictOptionsItem]) -> Tuple[List[Tuple[int, AnkiCard]], List[int]]:
    cards_to_push: List[Tuple[int, AnkiCard]] = []
    ids_to_delete: List[int] = []

    for curr_option in persisted_options:

        if curr_option.status == RequestStatus.OK and curr_option.selected:
            app_log.debug(f"selected option with id '{curr_option.dict_options_item_id}' "
                          f"with status {curr_option.status}")

            curr_card = AnkiCard(
                deck=curr_option.deck,
                front=curr_option.input,
                back=curr_option.output,
            )

            cards_to_push.append((
                curr_option.dict_options_item_id,
                curr_card
            ))

        elif curr_option.status != RequestStatus.SYNCED:
            ids_to_delete.append(curr_option.dict_options_item_id)

    return cards_to_push, ids_to_delete



# def _merge_duplicates(cards_to_push: List[Tuple[int, AnkiCard]]) -> :



def _push_in_batches(cards_to_push: List[Tuple[int, AnkiCard]], auth_headers: UnsignedAuthHeaders) -> None:
    for card_batch in chunked(cards_to_push, API_CONNECT_BATCH_SIZE):
        item_ids = [elem[0] for elem in card_batch]
        card_objects = [elem[1] for elem in card_batch]

        response_ok = WotdAnkiConnectFetcher.api_push_cards(card_objects, auth_headers)
        if response_ok:
            PersistenceService().update_items_status(item_ids, RequestStatus.SYNCED)
        else:
            app_log.error(f"not able to push card batch {card_batch}")


def _delete_elems_in_batches(ids_to_delete: List[int]):
    for id_batch in chunked(ids_to_delete, DB_BATCH_SIZE):
        app_log.debug(f'id_to_delete: {id_batch}')
        PersistenceService().delete_items_with_ids(id_batch)
