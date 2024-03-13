import os
from typing import List

import psycopg2

from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_options_response import DictOptionsResponse
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.info_request_default_dict_lang import InfoRequestDefaultDictLang
from src.data.dict_input.language import Language
from src.data.error.database_error import DatabaseError
from src.utils.logging_config import app_log


class PersistenceService:
    ENV_PASSWORD = 'POSTGRES_PASSWORD'
    ENV_USER = 'POSTGRES_USER'
    ENV_DB_NAME = 'POSTGRES_DB'

    def __init__(self):
        if (PersistenceService.ENV_PASSWORD not in os.environ) \
                or (PersistenceService.ENV_USER not in os.environ) \
                or (PersistenceService.ENV_DB_NAME not in os.environ):
            print('invalid environment - shutting down')
            # TODO handle this differently
            exit(1)

        self._conn = psycopg2.connect(
            database=os.environ[PersistenceService.ENV_DB_NAME],
            host="localhost",
            user=os.environ[PersistenceService.ENV_USER],
            password=os.environ[PersistenceService.ENV_PASSWORD],
            port="5432"
        )

        self._cursor = self._conn.cursor()

    # src: https://stackoverflow.com/questions/1263451/python-decorators-in-classes
    def _database_error_decorator(foo):
        def decorate(self, *args, **kwargs):
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
    def get_default_languages(self) -> InfoRequestDefaultDictLang:
        self._cursor.execute(
            "SELECT language.* FROM language "
            "INNER JOIN language_default ON language.language_id=language_default.dict_from_language_id;")
        entry = self._cursor.fetchone()
        app_log.debug(f"get_default_languages: {entry}")
        dict_default_from_language = Language(*entry)

        self._cursor.execute("SELECT language.* FROM language "
                             "INNER JOIN language_default ON language.language_id=language_default.dict_to_language_id;")
        entry = self._cursor.fetchone()
        dict_default_to_language = Language(*entry)

        req = InfoRequestDefaultDictLang(
            dict_default_to_language=dict_default_to_language,
            dict_default_from_language=dict_default_from_language
        )

        return req

    @_database_error_decorator  # type: ignore
    def save_dict_unique_request(self, request: DictRequest) -> DictRequest:
        duplicate: DictRequest | None = self.find_duplicate_dict_request(request)
        if duplicate:
            # TODO this is not a problem - delete this branch
            app_log.debug(f"found duplicate: {duplicate}")
            return duplicate

        app_log.debug(f"save_dict_request: {request}")

        sql_insert_string: str = (
            f"INSERT INTO dict_Request (user_id, from_language_uuid, to_language_uuid, input, ts) VALUES ("
            f"'{request.user_id}', "
            f"'{request.from_language_uuid}', "
            f"'{request.to_language_uuid}', "
            f"'{request.input}', "
            f"'{request.dict_request_ts}');")
        app_log.debug(f"sql string: {sql_insert_string}")
        self._cursor.execute(sql_insert_string)
        self._conn.commit()

        sql_select_string: str = f"SELECT * FROM dict_request WHERE input = '{request.input}'"
        self._cursor.execute(sql_select_string)
        entry = self._cursor.fetchone()
        app_log.debug(f"entry: {entry}")
        instance_with_id = DictRequest(*entry)
        app_log.debug(f"instance with id: {instance_with_id}")

        return instance_with_id

    def find_duplicate_dict_request(self, request: DictRequest) -> DictRequest | None:
        sql_select_clause: str = (f"SELECT * FROM dict_request "
                                  f"WHERE input = '{request.input.upper()}' "
                                  f"and user_id = '{request.user_id}' "
                                  f"and from_language_uuid = '{request.from_language_uuid}' "
                                  f"and to_language_uuid = '{request.to_language_uuid}';")
        app_log.debug(f'sql clause {sql_select_clause}')
        self._cursor.execute(sql_select_clause)
        sql_out = self._cursor.fetchone()
        if sql_out:
            return DictRequest(*sql_out)
        return None

    def find_duplicate_dict_options_response(self, request: DictRequest) -> DictOptionsResponse | None:
        sql_select_clause: str = (f"SELECT * FROM dict_options_response "
                                  f"WHERE input = '{request.input.upper()}' "
                                  f"and user_id = '{request.user_id}' "
                                  f"and from_language_uuid = '{request.from_language_uuid}' "
                                  f"and to_language_uuid = '{request.to_language_uuid}';")
        app_log.debug(f'sql clause {sql_select_clause}')
        self._cursor.execute(sql_select_clause)
        sql_out = self._cursor.fetchone()
        if sql_out:
            return DictRequest(*sql_out)
        return None

    @_database_error_decorator  # type: ignore
    def save_dict_options_response(self, dict_options_response: DictOptionsResponse):
        dict_options_response = self._update_plain_response(dict_options_response)
        dict_options_response = self._update_plain_options(dict_options_response)
        return dict_options_response

    def _update_plain_response(self, dict_options_response: DictOptionsResponse) -> DictOptionsResponse:
        """
        saves the wrapper object into the db and fetches the generated id into a new object
        """
        sql_insert = (f"INSERT INTO dict_options_response (dict_request_id, status, options_response_ts) VALUES ("
                      f"{dict_options_response.dict_request.dict_request_id}, "
                      f"'{dict_options_response.status.name.upper()}', "
                      f"'{dict_options_response.options_response_ts}' "
                      f") RETURNING dict_options_response_id;")
        self._cursor.execute(sql_insert)
        out = self._cursor.fetchone()[0]
        dict_options_response.dict_options_response_id = out
        self._conn.commit()

        return dict_options_response

    def _update_plain_options(self, dict_options_response: DictOptionsResponse) -> DictOptionsResponse:
        """
        saves the option objects into the db and fetches the generated id into a new object
        """
        response_id: int = dict_options_response.dict_options_response_id
        options: List[DictOptionsItem] = dict_options_response.options

        for curr_opt in options:
            sql_insert = (f"INSERT INTO dict_options_item (dict_options_response_id, input, output) VALUES ("
                          f"'{response_id}' ,"
                          f"'{curr_opt.input}' ,"
                          f"'{curr_opt.output}'"
                          f") RETURNING dict_options_item_id;")
            self._cursor.execute(sql_insert)
            curr_opt.dict_options_item_id = self._cursor.fetchone()[0]
            curr_opt.dict_options_response_id = response_id

        # sql_select = f"SELECT * FROM dict_options_item WHERE dict_options_response_id = {response_id};"
        # self._cursor.execute(sql_select)
        # updated_options = self._cursor.fetchall()
        self._conn.commit()

        # dict_options_response.options = updated_options
        # [DictOptionsItem(*curr_tuple) for curr_tuple in response_tuples]
        return dict_options_response


persistence_service = PersistenceService()
