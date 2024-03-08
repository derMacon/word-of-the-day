from flask import Blueprint, request, Response
from flask_cors import cross_origin

from src.logic import controller
from src.logic.controller import Controller
from src.utils.io_utils import extract_bearer_token
from src.utils.logging_config import log

main = Blueprint('main', __name__, url_prefix='/api/v1')
con = Controller()


@main.route("/login", methods=['POST'])
@cross_origin()
def login():
    log.debug('user called login endpoint')
    username = request.json.get('username')
    password = request.json.get('password')
    log.debug('username: %s', username)

    cont = Controller()
    token = cont.login(username, password)

    resp = Response()
    resp.headers['token'] = token
    return resp


@main.route("/list-decks")
@cross_origin()
def list_decks():
    log.debug("user called list decks endpoint")
    token = extract_bearer_token(request)
    log.debug(f"token: {token}")
    return con.list_decks(token)


def add_deck():
    pass
    # new_deckname = request.json.get('deckname')
    # log.debug('check if deck with name %s already exists', new_deckname)
