import sqlite3

from src.utils.io_utils import create_parent_dir
from src.utils.logging_config import app_log


class PersistenceService:
    SQLITE_FILE = './tmp/db/checklist-items.db'
    SQLITE_SCHEMA = './res/db/checklist-schema.sql'

    def __init__(self):
        create_parent_dir(PersistenceService.SQLITE_FILE)
        self._connection = sqlite3.connect(PersistenceService.SQLITE_FILE)
        # self._connection.set_trace_callback(sql_log.debug)
        self._cursor = self._connection.cursor()

        with open(PersistenceService.SQLITE_SCHEMA, 'r') as sql_schema:
            sql_commands = sql_schema.read()
            self._cursor.executescript(sql_commands)

    def set_items(self, checklist_name: str, item_list: [str]):
        app_log.debug(f"setting items for checklist {checklist_name}: {item_list}")
        checklist_id = self._translate_checklist_name(checklist_name)

        self._cursor.execute(f"DELETE FROM Item WHERE ChecklistId = {checklist_id}")
        app_log.debug(f"inserting {item_list} into Item table")
        for curr_item in item_list:
            self._cursor.execute(f"INSERT INTO Item (ItemName, ChecklistId) VALUES ('{curr_item}', {checklist_id})")

        self._connection.commit()

    def get_items(self, checklist_name: str):
        print(f"get items for {checklist_name}")
        app_log.debug(f"get items for {checklist_name}")
        checklist_id = self._translate_checklist_name(checklist_name)
        self._cursor.execute(f"SELECT ItemName FROM Item WHERE ChecklistId = {checklist_id}")
        item_names = self._unwrap_multiple_values()
        app_log.debug(f"items in checklist with id {checklist_id}: {item_names}")
        return item_names

    def _translate_checklist_name(self, checklist_name: str) -> int:
        self._cursor.execute(f"SELECT ChecklistId FROM Checklist WHERE ChecklistName = '{checklist_name}'")
        checklist_id = self._unwrap_single_value()
        app_log.debug(f"first check if checklist already present {checklist_id}")

        if not checklist_id:
            # app_log.debug(f"creating new checklist with name {checklist_name}")
            self._cursor.execute(f"INSERT INTO Checklist (ChecklistName) VALUES ('{checklist_name}')")
            self._cursor.execute(f"SELECT ChecklistId FROM Checklist WHERE ChecklistName = '{checklist_name}'")
            checklist_id = self._unwrap_single_value()

        app_log.debug(f"checklist_id {checklist_id} for checklist_name {checklist_name}")
        assert checklist_id
        return checklist_id

    def _unwrap_multiple_values(self):
        result = self._cursor.fetchall()
        if result:
            return [item[0] for item in result]
        return []

    def _unwrap_single_value(self):
        result = self._cursor.fetchmany(1)
        if result:
            return result[0][0]
        return None

    def teardown(self):
        self._connection.commit()
        self._cursor.close()
        self._connection.close()
