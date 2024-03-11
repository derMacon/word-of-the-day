import sqlite3
import pickle

from src.types.const.token_type import TokenType
from src.utils.logging_config import log


class PersistenceManager:

    def __init__(self):
        self._conn = sqlite3.connect('auth_cookies.db', check_same_thread=False)
        for member in TokenType:
            self._conn.execute(f'CREATE TABLE IF NOT EXISTS {member.value.db_table} (id TEXT PRIMARY KEY, data BLOB)')

    def insert_data(self, token_type: TokenType, key: str, data):
        log.debug('inserting blob for key: %s', key)
        pickled_data = pickle.dumps(data)
        self._conn.execute(f'INSERT INTO {token_type.value.db_table} (id, data) VALUES (?, ?)',
                           (key, sqlite3.Binary(pickled_data)))
        self._conn.commit()

    def read_data(self, token_type: TokenType, key: str):
        log.debug('reading blob for key: %s', key)
        cursor = self._conn.execute(f'SELECT data FROM {token_type.value.db_table} WHERE id = ?', (key,))
        result = cursor.fetchone()
        out = None

        if result:
            # Unpickle the data
            pickled_data = result[0]
            unpickled_data = pickle.loads(pickled_data)

            # Now, 'unpickled_data' contains the data associated with the given key
            log.debug(unpickled_data)
            out = unpickled_data
        else:
            log.error(f"No data found for key: {key}")
            # TODO exception

        return out
