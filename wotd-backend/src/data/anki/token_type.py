from enum import Enum


class HeaderType(str, Enum):
    SIGNED_USERNAME = 'X-Wotd-Username'
    SIGNED_UUID = 'X-Wotd-Uuid'
    UNSIGNED_USERNAME = 'UNSIGNED_USERNAME'
    UNSIGNED_UUID = 'UNSIGNED_UUID'
