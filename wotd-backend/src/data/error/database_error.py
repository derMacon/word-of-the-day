from src.utils.logging_config import app_log


class DatabaseError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


def database_error_decorator(func):
    def wrap():
        try:
            return func()
        except Exception as e:
            app_log.error(f"{e}")
            raise DatabaseError(e, e)
