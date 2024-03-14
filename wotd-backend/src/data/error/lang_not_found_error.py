from src.utils.logging_config import app_log


class LangNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
