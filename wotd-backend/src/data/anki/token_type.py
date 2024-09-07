from enum import Enum


class HeaderType(str, Enum):
    USERNAME = 'X-Wotd-Username'
    UUID = 'X-Wotd-Uuid'
