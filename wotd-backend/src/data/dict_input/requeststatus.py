from enum import Enum


class RequestStatus(str, Enum):
    """
    NOTE: needs to pass the string in order to be simply serializable
     in the context of the database connection
    """
    NOT_FOUND = 'NOT_FOUND'
    MISSPELLED = 'MISSPELLED'
    OK = 'OK'
    SYNCED = 'SYNCED'
