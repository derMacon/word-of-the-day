import time
from os import environ
from typing import List

from src.data.anki.anki_card import AnkiCard
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.status import Status
from src.logic.api_fetcher import api_fetcher
from src.service.persistence_service import persistence_service
from src.utils.logging_config import app_log


class HousekeepingController:

    def __init__(self):
        self._housekeeping_interval = int(environ.get('HOUSEKEEPING_INTERVAL_SEC'))
        if self._housekeeping_interval is None:
            app_log.error('no housekeeping interval specified - exiting housekeeping thread')
            exit(1)

    def run(self):
        while (True):
            self.sync_anki_cleanup()
            time.sleep(self._housekeeping_interval)

    def sync_anki_cleanup(self):
        persisted_options = persistence_service.find_expired_options(self._housekeeping_interval)
        for curr_option in persisted_options:
            if curr_option.status == Status.OK:
                app_log.debug(f"option with id '{curr_option.dict_options_item_id}' with status {curr_option.status}")
                # api_fetcher.push_card(AnkiCard())

        id_to_delete: List[int] = [curr_option.dict_options_item_id for curr_option in persisted_options]
        persistence_service.delete_items_with_ids(id_to_delete)
