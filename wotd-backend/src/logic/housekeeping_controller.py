from typing import List

from src.data.anki.anki_card import AnkiCard
from src.data.dict_input.anki_login_response_headers import AnkiLoginResponseHeaders
from src.data.dict_input.status import Status
from src.logic.anki_api_fetcher import anki_api_fetcher
from src.service.persistence_service import persistence_service
from src.utils.logging_config import app_log


def sync_anki_push(housekeeping_interval, auth_headers: AnkiLoginResponseHeaders):
    app_log.debug(f'sync anki push with interval: {housekeeping_interval}')

    persisted_options = persistence_service.find_expired_options(housekeeping_interval)
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
            anki_api_fetcher.push_card(card_input, auth_headers)

        ids_to_delete.append(curr_option.dict_options_item_id)

    app_log.debug(f'id_to_delete: {ids_to_delete}')
    persistence_service.delete_items_with_ids(ids_to_delete)
