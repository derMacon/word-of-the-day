from flask import request, Response
from flask_cors import cross_origin

from src.app import main
from src.logic.controller import Controller
from src.types.const.token_type import TokenType
from src.types.error.unauthorized_access_error import UnauthorizedAccessError
from src.utils.logging_config import log

controller = Controller()


@main.route("/login", methods=['POST'])
@cross_origin()
def login():
    log.debug('user called login endpoint')
    username = request.json.get('username')
    password = request.json.get('password')
    log.debug('username: %s', username)

    main_token, card_token = controller.login(username, password)

    resp = Response()
    resp.headers[TokenType.MAIN.value.header_key] = main_token
    resp.headers[TokenType.CARD.value.header_key] = card_token
    return resp


@main.route("/health")
@cross_origin()
def health():
    raise UnauthorizedAccessError('test')
    log.debug("api healthy")
    return 'running'


@main.route("/list-decks")
@cross_origin()
def list_decks():
    log.debug("user called list decks endpoint")
    return controller.list_decks()


@main.route("/add-deck")
@cross_origin()
def add_deck():
    deck = request.json.get('deck')
    log.debug(f"creating new deck with name: '{deck}'")
    controller.create_deck(deck)
    return ''


@main.route("/add-card")
@cross_origin()
def add_card():
    deck = request.json.get('deck')
    front = request.json.get('front')
    back = request.json.get('back')

    log.debug('deck: %s', deck)
    log.debug('front: %s', front)
    log.debug('back: %s', back)

    controller.add_card(deck, front, back)
    # TODO exception / error handler
    return '', 200
