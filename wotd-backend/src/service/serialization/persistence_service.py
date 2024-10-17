import os
import random
import threading
from typing import List

import psycopg2
from singleton_decorator import singleton

from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.env_collection import SensitiveEnv, ConnectionEnv
from src.data.dict_input.language_uuid import Language
from src.data.dict_input.requeststatus import RequestStatus
from src.data.error.database_error import DatabaseError
from src.data.error.lang_not_found_error import LangNotFoundError
from src.utils.logging_config import app_log, sql_log


# TODO use singleton decorator in other services / controllers

@singleton
class PersistenceService:
    _conn = None
    _cursor = None
    _available_languages: List[Language] = []

    def __init__(self):
        self._lock = threading.Lock()

        try:
            self._establish_db_connection()
        except DatabaseError as e:
            app_log.error(f"invalid db connection: '{e}'")

    def _establish_db_connection(self):
        if (SensitiveEnv.ENV_PASSWORD.value not in os.environ) \
                or (SensitiveEnv.ENV_USER.value not in os.environ) \
                or (SensitiveEnv.ENV_DB_NAME.value not in os.environ):
            app_log.error('invalid environment - shutting down')
            # TODO handle this differently
            exit(1)

        try:
            host = os.getenv(ConnectionEnv.ENV_DB_HOST.value, "localhost")
            port = os.getenv(ConnectionEnv.ENV_DB_PORT.value, "5432")
            app_log.debug(f"connecting to db: host - '{host}', port - '{port}'")

            self._conn = psycopg2.connect(
                database=os.environ[SensitiveEnv.ENV_DB_NAME.value],
                host=host,
                user=os.environ[SensitiveEnv.ENV_USER.value],
                password=os.environ[SensitiveEnv.ENV_PASSWORD.value],
                port=port,
                connect_timeout=3
            )
            self._cursor = self._conn.cursor()
        except Exception as e:
            self._conn = None
            self._cursor = None
            raise DatabaseError('invalid init', e)

    def db_connection_is_established(self):
        try:
            self._establish_db_connection()
        except DatabaseError as e:
            app_log.error(e)
            return False

        return self._cursor is not None

    # src: https://stackoverflow.com/questions/1263451/python-decorators-in-classes
    def _database_error_decorator(foo):  # TODO rename to 'instance' or something like that
        def decorate(self, *args, **kwargs):
            with self._lock:

                if not self.db_connection_is_established:
                    self._establish_db_connection()

                try:
                    out = foo(self, *args, **kwargs)
                    sql_log.debug(self._cursor.query)
                    return out
                except Exception as e:
                    app_log.error(f"{e}")
                    raise DatabaseError(e, e)
                    print("end magic")

        return decorate

    # TODO use this
    def teardown(self):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    @_database_error_decorator  # type: ignore
    def get_available_languages(self) -> List[Language]:
        self._cursor.execute("SELECT * FROM language;")

        for entry in self._cursor.fetchall():
            self._available_languages.append(Language(*entry))

        return self._available_languages

    def find_language_by_uuid(self, lang_uuid: str) -> List[Language]:
        for curr_lang in self.get_available_languages():
            if curr_lang.language_uuid == lang_uuid:
                return curr_lang
        raise LangNotFoundError(f'language with uuid {lang_uuid} not found')

    @_database_error_decorator  # type: ignore
    def insert_dict_request(self, dict_request: DictRequest, auth_headers: UnsignedAuthHeaders | None) -> DictRequest:
        """
        saves the option objects into the db and fetches the generated id into a new object
        """
        sql_insert = (
            "INSERT INTO dict_request (username, from_language_uuid, to_language_uuid, input, dict_request_ts) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING dict_request_id;")
        self._cursor.execute(sql_insert, (
            '' if auth_headers is None else auth_headers.username,
            dict_request.from_language_uuid,
            dict_request.to_language_uuid,
            dict_request.input,
            dict_request.dict_request_ts,
        ))
        dict_request.dict_request_id = self._cursor.fetchone()
        self._conn.commit()

        return dict_request

    @_database_error_decorator  # type: ignore
    def insert_dict_options(self, options: List[DictOptionsItem]) -> List[DictOptionsItem]:
        """
        saves the option objects into the db and fetches the generated id into a new object
        """
        for curr_opt in options:
            app_log.debug('persisting dict options')
            sql_insert = (
                "INSERT INTO dict_options_item (username, deck, input, output, selected, status, option_response_ts) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (deck, input, output) DO UPDATE SET status = %s "
                "RETURNING dict_options_item_id;"
            )
            self._cursor.execute(sql_insert, (
                curr_opt.username,
                curr_opt.deck,
                curr_opt.input,
                curr_opt.output,
                curr_opt.selected,
                curr_opt.status,
                curr_opt.option_response_ts,
                curr_opt.status,
            ))
            sql_log.debug(self._cursor.query)
            curr_opt.dict_options_item_id = self._cursor.fetchone()[0]

        self._conn.commit()
        return options

    def invalidate_dict_options(self, options: List[DictOptionsItem]) -> List[DictOptionsItem]:
        for curr_opt in options:
            curr_opt.dict_options_item_id = random.randint(-10000, -1)  # items with smaller ID than 0 are invalid
        return options

    @_database_error_decorator  # type: ignore
    def update_item_select(self, item_id: int):
        self._conn.commit()
        self._cursor.execute(
            "select selected from dict_options_item "
            f"where dict_options_item_id = {item_id};")
        selected_state = not self._cursor.fetchone()[0]
        app_log.debug(f"new selected state of item with id {item_id}: {selected_state}")

        # TODO use wildcard pattern instead of format string - do this everywhere
        sql_update = (f"UPDATE dict_options_item "
                      f"SET selected = {selected_state} "
                      f"WHERE dict_options_item_id = {item_id};")
        self._cursor.execute(sql_update)
        self._conn.commit()

    @_database_error_decorator  # type: ignore
    def update_items_status(self, item_ids: int, status: RequestStatus):
        if len(item_ids) == 0:
            app_log.debug('empty item id list - nothing to update')
            return

        id_placeholder = f"({','.join(map(str, item_ids))})"
        app_log.debug(f'sql update id placeholder: {id_placeholder}')

        self._conn.commit()

        # TODO use wildcard pattern instead of format string - do this everywhere
        sql_update = (f"UPDATE dict_options_item "
                      f"SET status = '{status}' "
                      f"WHERE dict_options_item_id IN {id_placeholder};")
        self._cursor.execute(sql_update)
        self._conn.commit()

    @_database_error_decorator  # type: ignore
    def find_expired_options_for_user(self, expiry_interval: int,
                                      auth_headers: UnsignedAuthHeaders) -> List[DictOptionsItem]:
        app_log.debug(f'find expired options for user with expiration interval of {expiry_interval} s for '
                      f'auth header {auth_headers}')
        sql_select = ("SET TIMEZONE TO 'Europe/Berlin';"
                      f"SELECT * FROM dict_options_item "
                      f"WHERE username = '{auth_headers.username}' "
                      f"AND option_response_ts < NOW() - interval '{expiry_interval} SECONDS';")
        app_log.debug('sql select: %s', sql_select)
        self._cursor.execute(sql_select)

        options: List[DictOptionsItem] = []
        response = self._cursor.fetchall()
        app_log.debug('response: %s', response)
        for entry in response:
            options.append(DictOptionsItem(*entry))

        app_log.debug('expired options: %s', options)
        return options

    @_database_error_decorator  # type: ignore
    def delete_items_with_ids(self, ids_to_delete: List[int]) -> List[DictOptionsItem]:
        if ids_to_delete:
            app_log.debug('delete options with ids: %s', ids_to_delete)
            delete_query = "DELETE FROM dict_options_item WHERE dict_options_item_id IN %s;"
            self._cursor.execute(delete_query, (tuple(ids_to_delete),))
            self._conn.commit()

    @_database_error_decorator  # type: ignore
    def get_all_dict_requests(self) -> List[DictRequest]:
        self._cursor.execute("SELECT * FROM dict_request;")
        return self._cursor.fetchall()

    # TODO delete this once it's clear that it's not being used
    # @_database_error_decorator  # type: ignore
    # def insert_anki_cards(self, cards: List[AnkiCard]) -> List[AnkiCard]:
    #     app_log.debug(f'persisting cards: {cards}')
    #
    #     for curr_card in cards:
    #         sql_insert = (
    #             "INSERT INTO anki_backlog (username, deck, front, back) "
    #             "VALUES (%s, %s, %s, %s) RETURNING anki_id;")
    #         self._cursor.execute(sql_insert, (
    #             curr_card.username,
    #             curr_card.deck,
    #             curr_card.front,
    #             curr_card.back
    #         ))
    #         app_log.debug('after insert')
    #         curr_card.anki_id = self._cursor.fetchone()[0]
    #         app_log.debug('after fetchone')
    #
    #     self._conn.commit()
    #     app_log.debug('after commit')
    #     return cards
    #
