import dataclasses
from typing import List
from typing import Tuple

from flask import jsonify, request, Response, make_response

from src.app import main
from src.controller.housekeeping_controller import trigger_housekeeping
from src.controller.web_controller import controller
from src.data.anki.anki_login_request import AnkiLoginRequest
from src.data.anki.token_type import HeaderType
from src.data.dict_input.anki_login_response_headers import AnkiLoginResponseHeaders
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.info_request_avail_dict_lang import InfoRequestAvailDictLang
from src.data.dict_input.option_select_request import OptionSelectRequest
from src.service.persistence_service import PersistenceService
from src.service.signature_service import SignatureService
from src.service.wotd_api_fetcher import anki_api_fetcher
from src.service.wotd_vnc_controller import WotdVncController
from src.utils.logging_config import app_log


@main.route("/health")
def health_check() -> Tuple[Response, int]:
    status = {
        'db_connection': PersistenceService().db_connection_is_established(),
        'anki_api_connection': anki_api_fetcher.health_check(),
        'wotd_api_connection': True,
    }
    app_log.debug(f"health: {status}")
    return jsonify(status), 200


@main.route("/anki/login", methods=['POST'])
def anki_login():
    anki_login_request: AnkiLoginRequest = AnkiLoginRequest(**request.get_json())

    # uuid = WotdVncController().login(
    #     username=anki_login_request.username,
    #     password=anki_login_request.password
    # )

    # signed_header_obj = SignatureService().create_signed_header_dict(
    #     username=anki_login_request.username,
    #     uuid=uuid
    # )

    signed_header_obj = SignatureService().create_signed_header_dict(
        username='testmail',
        uuid='testuuid'
    )

    app_log.debug(f"signed header obj: {signed_header_obj}")

    resp = make_response("login successful", 200)
    resp.headers.extend(signed_header_obj)

    # TODO delete this
    resp = Response()
    resp.headers[HeaderType.USERNAME] = 'testuser'
    resp.headers[HeaderType.UUID] = 'testuuid2'

    resp.headers.add('Access-Control-Expose-Headers',
                     HeaderType.MAIN.value.header_key
                     + ',' + HeaderType.CARD.value.header_key)

    return resp

    # return 'works', 200


@main.route("/dict/available-lang")
def dict_available_languages() -> Tuple[Response, int]:
    available_lang = PersistenceService().get_available_languages()
    app_log.debug(f"user queries available languages: {available_lang}")
    return jsonify(InfoRequestAvailDictLang(available_lang)), 200


@main.route("/dict/default-lang")
def dict_default_languages() -> Tuple[Response, int]:
    default_lang = PersistenceService().get_default_languages()
    app_log.debug(f"user queries default languages: {default_lang}")
    return jsonify(InfoRequestAvailDictLang(default_lang)), 200


@main.route("/dict/autocomplete-option", methods=['POST'])
def autocomplete_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    dict_request = DictRequest(**request_data)
    app_log.debug(f"dict request: {dict_request}")

    return jsonify(controller.autocomplete_dict_word(dict_request)), 200


@main.route("/dict/lookup-option", methods=['POST'])
def lookup_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    dict_request = DictRequest(**request_data)
    app_log.debug(f"dict request: {dict_request}")

    headers = _extract_headers()
    dict_options_response: List[DictOptionsItem] = controller.lookup_dict_word(dict_request, headers)

    json: Response = jsonify([dataclasses.asdict(curr_option) for curr_option in dict_options_response])
    app_log.debug('lookup response json: %s', json.get_json())

    trigger_housekeeping(headers)
    return json, 200


def _extract_headers():
    headers = None
    if HeaderType.MAIN.value.header_key in request.headers \
            and HeaderType.CARD.value.header_key in request.headers:
        app_log.debug('raw header: %s', request.headers)
        username = request.headers[HeaderType.USER.value.header_key]
        main_token = request.headers[HeaderType.MAIN.value.header_key]
        card_token = request.headers[HeaderType.CARD.value.header_key]
        headers = AnkiLoginResponseHeaders(username, main_token, card_token)
        app_log.debug('parsed header: %s', headers)
    else:
        app_log.debug(f'header not available: {request.headers}')
    return headers


@main.route("/anki/trigger-housekeeping")
def manually_trigger_housekeeping():
    app_log.debug('manually triggering housekeeping')
    headers = _extract_headers()
    trigger_housekeeping(headers)
    return ''


@main.route("/dict/select-option", methods=['POST'])
def select_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    selected_item_id: int = OptionSelectRequest(**request_data).selected_dict_options_item_id
    app_log.debug(f"selected item id: {selected_item_id}")

    output = {
        'select_successful': controller.select_dict_word(selected_item_id)
    }

    app_log.debug(f"json output: {output}")
    return jsonify(output), 200
