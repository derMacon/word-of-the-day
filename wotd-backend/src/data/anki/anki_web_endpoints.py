from enum import Enum


class AnkiWebEndpoints(str, Enum):
    LOGIN = 'https://ankiweb.net/account/login'
    LOGOUT = 'https://ankiweb.net/account/logout'
    DECKS = 'https://ankiweb.net/decks'
    ADD = 'https://ankiweb.net/add'
    ALL = '*'
