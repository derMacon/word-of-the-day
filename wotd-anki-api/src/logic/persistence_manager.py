import sqlite3
import pickle

from src.utils.logging_config import log


class PersistenceManager:

    def __init__(self):
        self._conn = sqlite3.connect('auth_cookies.db', check_same_thread=False)
        self._conn.execute('CREATE TABLE IF NOT EXISTS pickled_data (id TEXT PRIMARY KEY, data BLOB)')

    def insert_data(self, key: str, data):
        log.debug('inserting blob for key: %s', key)
        pickled_data = pickle.dumps(data)
        self._conn.execute('INSERT INTO pickled_data (id, data) VALUES (?, ?)',
                           (key, sqlite3.Binary(pickled_data)))
        self._conn.commit()

    def read_data(self, key: str):
        log.debug('reading blob for key: %s', key)
        cursor = self._conn.execute('SELECT data FROM pickled_data WHERE id = ?', (key,))
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

