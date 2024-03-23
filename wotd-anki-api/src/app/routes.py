import threading
from time import sleep

from flask import request, Response
from flask_cors import cross_origin

from src.app import main
from src.logic.controller import Controller
from src.types.const.token_type import TokenType
from src.utils.logging_config import log
from src.utils.thread_safe_counter import ThreadSafeCounter

ADD_CARD_MAX_CONSECUTIVE_PUSHES = 4
COOL_DOWN_SECS = 3

controller = Controller()
lock = threading.Lock()
cool_down_counter = ThreadSafeCounter()

@main.route("/login", methods=['POST'])
@cross_origin()
def login():
    with lock: # TODO locking via server config not explicit in the code
        log.debug('user called login endpoint')
        username = request.json.get('username')
        password = request.json.get('password')
        log.debug('username: %s', username)

        main_token, card_token = controller.login(username, password)

        resp = Response()
        resp.headers[TokenType.MAIN.value.header_key] = main_token
        resp.headers[TokenType.CARD.value.header_key] = card_token

        resp.headers.add('Access-Control-Expose-Headers',
                         TokenType.MAIN.value.header_key
                         + ',' + TokenType.CARD.value.header_key)
        return resp


@main.route("/health")
@cross_origin()
def health():
    log.debug("api healthy")
    return 'running'


@main.route("/list-decks")
@cross_origin()
def list_decks():
    with lock:
        log.debug("user called list decks endpoint")
        return controller.list_decks()


@main.route("/add-deck")
@cross_origin()
def add_deck():
    with lock:
        deck = request.json.get('deck')
        log.debug(f"creating new deck with name: '{deck}'")
        controller.create_deck(deck)
        return ''


@main.route("/add-card")
@cross_origin()
def add_card():
    with lock:
        log.debug('user called add card')

        if cool_down_counter.increment() % ADD_CARD_MAX_CONSECUTIVE_PUSHES == 0:
            log.debug(f'anki api is only able to push {ADD_CARD_MAX_CONSECUTIVE_PUSHES} cards consecutively')
            sleep(COOL_DOWN_SECS)

        deck = request.json.get('deck')
        front = request.json.get('front')
        back = request.json.get('back')

        log.debug('deck: %s', deck)
        log.debug('front: %s', front)
        log.debug('back: %s', back)

        controller.add_card(deck, front, back)
        # TODO exception / error handler
        return '', 200
