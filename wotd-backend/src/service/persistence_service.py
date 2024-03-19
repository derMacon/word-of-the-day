import os
import threading
from typing import List

import psycopg2
from singleton_decorator import singleton

from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.info_request_default_dict_lang import InfoRequestDefaultDictLang
from src.data.dict_input.language import Language
from src.data.dict_input.sensitive_env import SensitiveEnv
from src.data.dict_input.status import Status
from src.data.error.database_error import DatabaseError
from src.data.error.lang_not_found_error import LangNotFoundError
from src.utils.logging_config import app_log


# TODO use singleton decorator in other services / controllers

@singleton
class PersistenceService:
    _conn = None
    _cursor = None

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
            print('invalid environment - shutting down')
            # TODO handle this differently
            exit(1)

        try:
            self._conn = psycopg2.connect(
                database=os.environ[SensitiveEnv.ENV_DB_NAME.value],
                host="localhost",
                user=os.environ[SensitiveEnv.ENV_USER.value],
                password=os.environ[SensitiveEnv.ENV_PASSWORD.value],
                port="5432"
            )
            self._cursor = self._conn.cursor()
        except Exception as e:
            self._conn = None
            self._cursor = None
            raise DatabaseError('invalid init', e)

    def connection_is_established(self):
        try:
            self._establish_db_connection()
        except DatabaseError as e:
            app_log.error(e)

        return self._cursor is not None

    # src: https://stackoverflow.com/questions/1263451/python-decorators-in-classes
    def _database_error_decorator(foo):  # TODO rename to 'instance' or something like that
        def decorate(self, *args, **kwargs):
            with self._lock:

                if not self.connection_is_established:
                    self._establish_db_connection()

                try:
                    return foo(self, *args, **kwargs)
                except Exception as e:
                    app_log.error(f"{e}")
                    raise DatabaseError(e, e)
                    print("end magic")

        return decorate

    def teardown(self):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    @_database_error_decorator  # type: ignore
    def get_available_languages(self) -> List[Language]:
        self._cursor.execute("SELECT * FROM language;")

        languages: List[Language] = []
        for entry in self._cursor.fetchall():
            languages.append(Language(*entry))

        return languages

    @_database_error_decorator  # type: ignore
    def find_language_by_uuid(self, lang_uuid: str) -> List[Language]:
        for curr_lang in self.get_available_languages():
            if curr_lang.language_uuid == lang_uuid:
                return curr_lang
        raise LangNotFoundError(f'language with uuid {lang_uuid} not found')

    @_database_error_decorator  # type: ignore
    def get_default_languages(self) -> InfoRequestDefaultDictLang:
        self._cursor.execute(
            "SELECT language.* FROM language "
            "INNER JOIN language_default ON language.language_uuid=language_default.dict_from_language_uuid;")
        entry = self._cursor.fetchone()
        app_log.debug(f"get_default_languages: {entry}")
        dict_default_from_language = Language(*entry)

        self._cursor.execute("SELECT language.* FROM language "
                             "INNER JOIN language_default ON language.language_uuid=language_default.dict_to_language_uuid;")
        entry = self._cursor.fetchone()
        dict_default_to_language = Language(*entry)

        req = InfoRequestDefaultDictLang(
            dict_default_to_language=dict_default_to_language,
            dict_default_from_language=dict_default_from_language
        )

        return req

    def insert_dict_options(self, options: List[DictOptionsItem]) -> List[DictOptionsItem]:
        """
        saves the option objects into the db and fetches the generated id into a new object
        """
        for curr_opt in options:
            sql_insert = ("INSERT INTO dict_options_item (deck, input, output, selected, status, option_response_ts) "
                          "VALUES (%s, %s, %s, %s, %s, %s) RETURNING dict_options_item_id;")
            self._cursor.execute(sql_insert, (
                curr_opt.deck,
                curr_opt.input,
                curr_opt.output,
                curr_opt.selected,
                curr_opt.status,
                curr_opt.option_response_ts,
            ))
            curr_opt.dict_options_item_id = self._cursor.fetchone()[0]

        self._conn.commit()
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
    def update_item_status(self, item_id: int, status: Status):
        self._conn.commit()
        self._cursor.execute(
            "select selected from dict_options_item "
            f"where dict_options_item_id = {item_id};")
        selected_state = not self._cursor.fetchone()[0]
        app_log.debug(f"new selected state of item with id {item_id}: {selected_state}")

        # TODO use wildcard pattern instead of format string - do this everywhere
        sql_update = (f"UPDATE dict_options_item "
                      f"SET status = '{status}' "
                      f"WHERE dict_options_item_id = {item_id};")
        self._cursor.execute(sql_update)
        self._conn.commit()

    @_database_error_decorator  # type: ignore
    def find_expired_options(self, expiry_interval: int) -> List[DictOptionsItem]:
        sql_select = ("SET TIMEZONE TO 'Europe/Berlin';"
                      f"SELECT * FROM dict_options_item "
                      f"WHERE option_response_ts < NOW() - interval '{expiry_interval} SECONDS';")
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
