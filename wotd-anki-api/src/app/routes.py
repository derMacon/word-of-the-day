from flask import Blueprint, request, Response
from flask_cors import cross_origin

from src.logic import controller
from src.logic.controller import Controller
from src.utils.logging_config import log

main = Blueprint('main', __name__, url_prefix='/api/v1')
controller = Controller()


@main.route("/login", methods=['POST'])
@cross_origin()
def login():
    log.debug('user called login endpoint')
    username = request.json.get('username')
    password = request.json.get('password')
    log.debug('username: %s', username)

    token = controller.login(username, password)

    resp = Response()
    resp.headers['token'] = token
    return resp
    # resp.headers['Authorization'] = f'Bearer {token}'



@main.route("/health")
@cross_origin()
def health():
    log.debug("api healthy")
    return 'running'

@main.route("/list-decks")
@cross_origin()
def list_decks():
    log.debug("user called list decks endpoint")
    return controller.list_decks()


def add_deck():
    pass
    # new_deckname = request.json.get('deckname')
    # log.debug('check if deck with name %s already exists', new_deckname)


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
    return 200
