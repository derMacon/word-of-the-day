from enum import Enum


class Status(Enum):
    NOT_FOUND = 1
    MISSPELLED = 2
    OK = 3
    SYNCED = 4
