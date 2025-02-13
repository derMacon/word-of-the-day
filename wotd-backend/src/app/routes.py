import dataclasses
import io
import json
import os
from datetime import datetime, time
from typing import List
from typing import Tuple

from flask import jsonify, request, Response, send_file

from src.app import main
from src.controller.housekeeping_controller import trigger_housekeeping, MUTEX, trigger_complete_cycle
from src.controller.web_controller import WebController, health_check_wrapper
from src.data.anki.anki_login_request import AnkiLoginRequest
from src.data.anki.token_type import HeaderType
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.env_collection import GeneralEnv
from src.data.dict_input.info_request_avail_dict_lang import InfoResponseAvailDictLang
from src.data.dict_input.info_response_housekeeping import InfoResponseHousekeeping
from src.data.dict_input.info_response_user_logged_in import InfoResponseUserLoggedIn
from src.data.dict_input.option_select_request import OptionSelectRequest
from src.service.serialization.signature_service import SignatureService
from src.utils.logging_config import app_log

LOGIN_MAX_RETRIES = 3


@main.route("/health")
def health_check() -> Tuple[Response, int]:
    return jsonify(health_check_wrapper()), 200


@main.route("/version")
def version() -> Tuple[Response, int]:
    wotd_version = os.getenv(GeneralEnv.ENV_WOTD_VERSION.value, 'no version specified')
    app_log.info(f'wotd version: {wotd_version}')
    return jsonify({'version': wotd_version}), 200


@main.route("/anki/login", methods=['POST'])
def anki_login():
    with MUTEX:
        anki_login_request: AnkiLoginRequest = AnkiLoginRequest(**request.get_json())
        uuid = WebController().login(anki_login_request)

        signed_header_obj = SignatureService().create_signed_header_dict(
            username=anki_login_request.username,
            uuid=uuid
        )

        app_log.debug(f"signed header obj: {signed_header_obj}")

        resp = Response()
        resp.headers.extend(signed_header_obj)
        resp.headers.add('Access-Control-Expose-Headers',
                         f"{HeaderType.SIGNED_USERNAME.value}, {HeaderType.SIGNED_UUID.value}")

        return resp


@main.route("/dict/available-lang")
def dict_available_languages() -> Tuple[Response, int]:
    available_lang = WebController().dict_available_languages_cached()
    app_log.debug(f"user queries available languages: {available_lang}")
    return jsonify(InfoResponseAvailDictLang(available_lang)), 200


@main.route("/dict/autocomplete-option", methods=['POST'])
def autocomplete_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    dict_request = DictRequest(**request_data)
    app_log.debug(f"dict request: {dict_request}")

    return jsonify(WebController().autocomplete_dict_word(dict_request)), 200


@main.route("/dict/lookup-option", methods=['POST'])
def lookup_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    dict_request = DictRequest(**request_data)
    app_log.debug(f"dict request: {dict_request}")

    unsigned_auth_headers: UnsignedAuthHeaders | None = _extract_unsigned_headers()
    dict_options_response: List[DictOptionsItem] = WebController().lookup_dict_word(dict_request, unsigned_auth_headers)

    json: Response = jsonify([dataclasses.asdict(curr_option) for curr_option in dict_options_response])
    app_log.debug('lookup response json: %s', json.get_json())

    return json, 200


@main.route("/dict/request-log")
def dict_request_log():
    app_log.debug('manually trigger request log retrieval')
    json_str: str = json.dumps(WebController().get_request_log(), default=str)
    memory_file = io.StringIO(json_str)
    return send_file(
        io.BytesIO(memory_file.getvalue().encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name='requests.json'
    )


def _extract_unsigned_headers() -> UnsignedAuthHeaders:
    auth_headers = None
    if HeaderType.SIGNED_USERNAME.value in request.headers \
            and HeaderType.SIGNED_UUID.value in request.headers:
        app_log.debug('raw header: %s', request.headers)
        signed_username = request.headers[HeaderType.SIGNED_USERNAME.value]
        signed_uuid = request.headers[HeaderType.SIGNED_UUID.value]

        sign_service: SignatureService = SignatureService()
        unsigned_username = sign_service.unsign(signed_username)
        unsigned_uuid = sign_service.unsign(signed_uuid)

        auth_headers: UnsignedAuthHeaders = UnsignedAuthHeaders(unsigned_username, unsigned_uuid)
        app_log.debug('parsed auth headers: %s', auth_headers)
    else:
        app_log.debug(f'header not available: {request.headers}')
    return auth_headers


@main.route("/anki/user-is-logged-in")
def anki_user_is_logged_in():
    headers: UnsignedAuthHeaders | None = _extract_unsigned_headers()
    app_log.debug(f'checking if user is logged in: {headers}')
    user_is_logged_in = WebController().anki_user_logged_in(headers)
    app_log.debug(f'user is logged in: {user_is_logged_in}')
    return jsonify(InfoResponseUserLoggedIn(user_is_logged_in)), 200


@main.route("/anki/trigger-housekeeping")
def manually_trigger_housekeeping():
    app_log.debug('manually triggering housekeeping')
    headers: UnsignedAuthHeaders = _extract_unsigned_headers()
    trigger_housekeeping(headers)
    return '', 200


@main.route("/anki/trigger-cycle")
def manually_trigger_cycle():
    """
    difference to the individual housekeeping trigger: trigger housekeeping for all persisted auth headers
    @return: empty http response
    """
    app_log.debug('manually trigger cycle')
    trigger_complete_cycle()
    return '', 200


@main.route("/anki/housekeeping-info")
def housekeeping_info():
    today = datetime.now().date()
    midnight = datetime.combine(today, time.min)
    housekeeping_info_dummy = InfoResponseHousekeeping(midnight)
    app_log.debug(f'user requested housekeeping info: {housekeeping_info_dummy}')
    return jsonify(housekeeping_info_dummy), 200


@main.route("/dict/select-option", methods=['POST'])
def select_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    selected_item_id: int = OptionSelectRequest(**request_data).selected_dict_options_item_id
    app_log.debug(f"selected item id: {selected_item_id}")

    output = {
        'select_successful': WebController().select_dict_word(selected_item_id)
    }

    app_log.debug(f"json output: {output}")
    return jsonify(output), 200
