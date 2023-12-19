import os
from typing import List, Callable

import psycopg2

from src.data.error.database_error import DatabaseError
from src.data.data_types import DictRequest, DictOptionsResponse, Language, InfoRequestDefaultDictLang, LanguageUUID
from src.utils.logging_config import app_log


class PersistenceService:
    ENV_PASSWORD = 'POSTGRES_PASSWORD'
    ENV_USER = 'POSTGRES_USER'
    ENV_DB_NAME = 'POSTGRES_DB'

    # SQLITE_FILE = './tmp/db/checklist-items.db'
    # SQLITE_SCHEMA = './res/db/checklist-schema.sql'
    #
    # def __init__(self):
    #     create_parent_dir(PersistenceService.SQLITE_FILE)
    #     self._connection = sqlite3.connect(PersistenceService.SQLITE_FILE)
    #     # self._connection.set_trace_callback(sql_log.debug)
    #     self._cursor = self._connection.cursor()
    #
    #     with open(PersistenceService.SQLITE_SCHEMA, 'r') as sql_schema:
    #         sql_commands = sql_schema.read()
    #         self._cursor.executescript(sql_commands)
    #
    # def set_items(self, checklist_name: str, item_list: [str]):
    #     app_log.debug(f"setting items for checklist {checklist_name}: {item_list}")
    #     checklist_id = self._translate_checklist_name(checklist_name)
    #
    #     self._cursor.execute(f"DELETE FROM Item WHERE ChecklistId = {checklist_id}")
    #     app_log.debug(f"inserting {item_list} into Item table")
    #     for curr_item in item_list:
    #         self._cursor.execute(f"INSERT INTO Item (ItemName, ChecklistId) VALUES ('{curr_item}', {checklist_id})")
    #
    #     self._connection.commit()
    #
    # def get_items(self, checklist_name: str):
    #     print(f"get items for {checklist_name}")
    #     app_log.debug(f"get items for {checklist_name}")
    #     checklist_id = self._translate_checklist_name(checklist_name)
    #     self._cursor.execute(f"SELECT ItemName FROM Item WHERE ChecklistId = {checklist_id}")
    #     item_names = self._unwrap_multiple_values()
    #     app_log.debug(f"items in checklist with id {checklist_id}: {item_names}")
    #     return item_names
    #
    # def _translate_checklist_name(self, checklist_name: str) -> int:
    #     self._cursor.execute(f"SELECT ChecklistId FROM Checklist WHERE ChecklistName = '{checklist_name}'")
    #     checklist_id = self._unwrap_single_value()
    #     app_log.debug(f"first check if checklist already present {checklist_id}")
    #
    #     if not checklist_id:
    #         # app_log.debug(f"creating new checklist with name {checklist_name}")
    #         self._cursor.execute(f"INSERT INTO Checklist (ChecklistName) VALUES ('{checklist_name}')")
    #         self._cursor.execute(f"SELECT ChecklistId FROM Checklist WHERE ChecklistName = '{checklist_name}'")
    #         checklist_id = self._unwrap_single_value()
    #
    #     app_log.debug(f"checklist_id {checklist_id} for checklist_name {checklist_name}")
    #     assert checklist_id
    #     return checklist_id
    #
    # def _unwrap_multiple_values(self):
    #     result = self._cursor.fetchall()
    #     if result:
    #         return [item[0] for item in result]
    #     return []
    #
    # def _unwrap_single_value(self):
    #     result = self._cursor.fetchmany(1)
    #     if result:
    #         return result[0][0]
    #     return None
    #
    # def teardown(self):
    #     self._connection.commit()
    #     self._cursor.close()
    #     self._connection.close()

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
        self._connection.commit()
        self._cursor.close()
        self._connection.close()

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
    def save_dict_request(self, dict_request: DictRequest) -> DictRequest:
        # TODO
        app_log.debug(f"save_dict_request: {dict_request}")

        sql_insert_string: str = f"INSERT INTO dict_Request (from_language_uuid, to_language_uuid, input) VALUES (\
            '{dict_request.from_language_uuid}', '{dict_request.to_language_uuid}', '{dict_request.input}');"
        app_log.debug(f"sql string: {sql_insert_string}")
        self._cursor.execute(sql_insert_string)
        self._conn.commit()

        sql_select_string: str = f"SELECT * FROM dict_request WHERE input = '{dict_request.input}'"
        self._cursor.execute(sql_select_string)
        entry = self._cursor.fetchone()
        app_log.debug(f"entry: {entry}")
        instance_with_id = DictRequest(*entry)
        app_log.debug(f"instance with id: {instance_with_id}")

        return instance_with_id

    @_database_error_decorator
    def save_dict_options_response(self, entry_id: int, dict_options_response: DictOptionsResponse):
        print(f"TOOD do not generate new id use: {dict_options_response.id}")


persistence_service = PersistenceService()
