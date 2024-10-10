import copy
import csv
import logging
import os
import threading
from threading import Lock
from time import sleep
from typing import List, Tuple

from more_itertools import chunked, collapse

from src.data.anki.anki_card import AnkiCard, MERGING_SEPERATOR
from src.data.dict_input import now
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.requeststatus import RequestStatus
from src.data.error.database_error import DatabaseError
from src.data.error.missing_headers_error import MissingHeadersError
from src.service.anki_connect.anki_connect_fetcher import AnkiConnectFetcher
from src.service.serialization.persistence_service import PersistenceService
from src.utils.logging_config import app_log

MAX_CONNECTION_TRIES = 3
API_CONNECT_BATCH_SIZE = 10
DB_BATCH_SIZE = 100
FALLBACK_CSV_PATH = 'res/fallback-decks/csv'
FALLBACK_DECK_NAME = 'wotd::fallback'
FALLBACK_CSV_DEFAULT_SEPERATOR = ';'
FALLBACK_DECK_MAX_SIZE = 500

MUTEX = Lock()


def trigger_housekeeping(auth_headers: UnsignedAuthHeaders):
    if auth_headers is None:
        raise MissingHeadersError('missing headers when syncing anki push')

    delay_sec = float(os.environ.get('HOUSEKEEPING_INTERVAL_SEC', 0)  # TODO dont hardcode this
    app_log.debug(f'triggering housekeeping in {delay_sec} secs')
    threading.Timer(delay_sec, sync_anki_push, args=(delay_sec, auth_headers,)).start()


def sync_anki_push(housekeeping_interval, auth_headers: UnsignedAuthHeaders):
    try:
        with MUTEX:
            app_log.debug(f'sync anki push with delay {housekeeping_interval} s and {auth_headers}')

            _wait_for_connection(housekeeping_interval)

            if PersistenceService().db_connection_is_established() and AnkiConnectFetcher.health_check():
                _push_data(housekeeping_interval, auth_headers)
            else:
                app_log.debug('not possible to push data to anki connect api - try pushing with next cleanup job')

            app_log.debug('finished housekeeping')
    except DatabaseError as e:
        app_log.error(f"error: '{e}'")


def _wait_for_connection(housekeeping_interval):
    error_cnt = 0
    while not PersistenceService().db_connection_is_established() and error_cnt < MAX_CONNECTION_TRIES:
        error_cnt = error_cnt + 1
        sleep(housekeeping_interval)


def _push_data(housekeeping_interval, auth_headers: UnsignedAuthHeaders):
    app_log.debug('preparing data to push to anki connect')
    _push_fallback_decks(auth_headers)
    _push_dict_lookups(housekeeping_interval, auth_headers)


def _push_fallback_decks(auth_headers: UnsignedAuthHeaders):
    if not AnkiConnectFetcher.check_if_deck_is_present(FALLBACK_DECK_NAME):
        app_log.debug(f'fallback deck name not present: {FALLBACK_DECK_NAME}')
        cards: List[AnkiCard] = _create_fallback_deck_cards(auth_headers.username)
        _push_anki_connect_in_batches(cards, auth_headers)


def _create_fallback_deck_cards(username: str) -> List[AnkiCard]:
    cards: List[AnkiCard] = []

    for file in os.listdir(FALLBACK_CSV_PATH):
        app_log.debug(f'csv file to import: {file}')

        for row in _read_csv(os.path.join(FALLBACK_CSV_PATH, file)):
            front, back = row
            cards.append(AnkiCard(
                deck=FALLBACK_DECK_NAME,
                front=front,
                back=back,
                ts=now()
            ))

    return cards[:FALLBACK_DECK_MAX_SIZE]


def _read_csv(file_path: str, seperator: str = FALLBACK_CSV_DEFAULT_SEPERATOR) -> List[Tuple[str, str]]:
    output: List[Tuple[str, str]] = []
    with open(file_path, mode='r', newline='', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=seperator)

        for row in csv_reader:
            front, back = row
            output.append((front, back))

    return output


def _push_dict_lookups(housekeeping_interval, auth_headers: UnsignedAuthHeaders):
    app_log.debug('push dict lookups')
    persisted_options: List[DictOptionsItem] = PersistenceService().find_expired_options_for_user(
        housekeeping_interval,
        auth_headers
    )

    cards_to_push, ids_to_delete = _filter_elems_to_push(persisted_options)
    _create_decks(cards_to_push)
    duplicate_remote_cards = _find_pushed_duplicates(cards_to_push)
    _delete_pushed_duplicates(duplicate_remote_cards)

    cards_to_push.extend(duplicate_remote_cards)
    _delete_exact_duplicates(cards_to_push)
    _merge_duplicate_fronts(cards_to_push)

    # TODO flip and append cards to create more
    _sort_by_ts(cards_to_push)
    _push_anki_connect_in_batches(cards_to_push, auth_headers)
    # _persist_anki_cards_in_batches(cards_to_push)
    _delete_elems_in_batches(ids_to_delete)


def _find_pushed_duplicates(anki_cards: List[AnkiCard]) -> List[AnkiCard]:
    card_status = AnkiConnectFetcher._cards_can_be_added(anki_cards)
    duplicates: List[AnkiCard] = []
    for curr_card, card_can_be_added in zip(anki_cards, card_status):
        if not card_can_be_added:
            anki_card_id = AnkiConnectFetcher._find_pushed_anki_id(curr_card)
            duplicates.append(AnkiConnectFetcher._get_card_by_id(anki_card_id))

    return duplicates


def _delete_pushed_duplicates(duplicate_cards: List[AnkiCard]) -> None:
    # TODO also persist in db before deleting them remote - in selectable items db table

    # TODO wouldn't it be nice to have this batching mechanism in the called method itself?
    for curr_card_batch in chunked(duplicate_cards, API_CONNECT_BATCH_SIZE):
        AnkiConnectFetcher._delete_cards(curr_card_batch)


def _filter_elems_to_push(persisted_options: List[DictOptionsItem]) -> Tuple[List[AnkiCard], List[int]]:
    cards_to_push: List[AnkiCard] = []
    ids_to_delete: List[int] = []

    for curr_option in persisted_options:

        if curr_option.status == RequestStatus.OK and curr_option.selected:
            app_log.debug(f"selected option with id '{curr_option.dict_options_item_id}' "
                          f"with status {curr_option.status}")

            cards_to_push.append(
                AnkiCard(
                    item_ids=[curr_option.dict_options_item_id],
                    deck=curr_option.deck,
                    front=curr_option.input,
                    back=curr_option.output,
                    ts=curr_option.option_response_ts
                )
            )

        elif curr_option.status != RequestStatus.SYNCED:
            ids_to_delete.append(curr_option.dict_options_item_id)

    return cards_to_push, ids_to_delete


def _create_decks(anki_cards: List[AnkiCard]) -> None:
    for deck in set([opt.deck for opt in anki_cards]):
        if not AnkiConnectFetcher.check_if_deck_is_present(deck):
            app_log.debug(f"deck '{deck}' not present need to create it")
            AnkiConnectFetcher._create_single_deck(deck)


def _sort_by_ts(cards_to_push: List[AnkiCard]) -> None:
    # def _sort_by_ts(cards_to_push: List[AnkiCard]) -> List[AnkiCard]:
    # sorted(cards_to_push, key=lambda card: card.ts)
    cards_to_push.sort(key=lambda card: card.ts)


def _delete_exact_duplicates(cards_to_push: List[AnkiCard]) -> None:
    unique_lst_copy = list(set(copy.deepcopy(cards_to_push)))
    cards_to_push.clear()
    cards_to_push.extend(unique_lst_copy)


def _merge_duplicate_fronts(cards_to_push: List[AnkiCard]) -> None:
    # used_decks = list(set([card.deck for card in cards_to_push]))
    # deck_mapping = {}
    # for deckname in used_decks:
    #     cards_from_deck = [card for card in cards_to_push if card.deck == deckname]
    #     deck_mapping.setdefault(deckname, []).append(cards_from_deck)

    mapping: dict[str, List[AnkiCard]] = {}
    for card in cards_to_push:
        tuple_key_identifier = (card.deck, card.front)
        mapping.setdefault(tuple_key_identifier, []).append(card)

    merged_stack: List[AnkiCard] = []
    duplicates: list[AnkiCard]
    for _, duplicates in mapping.items():
        assert len(duplicates) > 0
        merged_elems = duplicates[0].merge_cards(duplicates[1:])
        merged_stack.append(merged_elems)

    cards_to_push.clear()
    cards_to_push.extend(merged_stack)


def _push_anki_connect_in_batches(cards_to_push: List[AnkiCard], auth_headers: UnsignedAuthHeaders) -> None:
    for card_batch in chunked(cards_to_push, API_CONNECT_BATCH_SIZE):
        item_ids = list(collapse([elem.item_ids for elem in card_batch]))

        push_response = AnkiConnectFetcher.api_push_cards(card_batch, auth_headers)
        if push_response is not None and push_response.error is None:

            for (generated_id, anki_card) in zip(push_response.result, cards_to_push):
                anki_card.anki_id = generated_id

            PersistenceService().update_items_status(item_ids, RequestStatus.SYNCED)
        else:
            app_log.error(f"not able to push card batch {card_batch} - push response: {push_response}")


def _persist_anki_cards_in_batches(cards: List[AnkiCard]) -> None:
    # TODO wouldn't it be nice to have this batching mechanism in the called method itself?
    # for card_batch in chunked(cards, DB_BATCH_SIZE):
    #     PersistenceService().insert_anki_cards(card_batch)
    pass


def _delete_elems_in_batches(ids_to_delete: List[int]):
    # TODO wouldn't it be nice to have this batching mechanism in the called method itself?
    for id_batch in chunked(ids_to_delete, DB_BATCH_SIZE):
        app_log.debug(f'id_to_delete: {id_batch}')
        PersistenceService().delete_items_with_ids(id_batch)
