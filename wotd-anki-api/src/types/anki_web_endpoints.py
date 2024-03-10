from enum import Enum


class AnkiWebEndpoints(str, Enum):
    LOGIN = 'https://ankiweb.net/account/login'
    DECKS = 'https://ankiweb.net/decks'
    ADD = 'https://ankiweb.net/add'
