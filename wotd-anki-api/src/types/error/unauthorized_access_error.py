from src.utils.logging_config import log


class UnauthorizedAccessError(Exception):
    def __init__(self, message):
        super().__init__(message)
