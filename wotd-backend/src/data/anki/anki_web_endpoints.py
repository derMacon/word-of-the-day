from enum import Enum


# TODO do we need these?
class AnkiWebEndpoints(str, Enum):
    LOGIN = 'https://ankiweb.net/account/login'
    LOGOUT = 'https://ankiweb.net/account/logout'
    DECKS = 'https://ankiweb.net/decks'
    ADD = 'https://ankiweb.net/add'
    ALL = '*'
