from enum import Enum


class HeaderType(str, Enum):
    USERNAME = 'X-Username'
    UUID = 'X-Uuid'
