from typing import List
import dataclasses
from typing import Tuple

from flask import jsonify, request, Response

from src.app import main
from src.data.dict_input.dict_options_item import DictOptionsItem
from src.data.dict_input.dict_request import DictRequest
from src.data.dict_input.info_request_avail_dict_lang import InfoRequestAvailDictLang
from src.data.dict_input.option_select_request import OptionSelectRequest
from src.logic.web_controller import controller
from src.service.persistence_service import persistence_service
from src.utils.logging_config import app_log


@main.route("/health")
def test_log() -> Tuple[Response, int]:
    status = {'status': 'running'}
    app_log.debug(f"health: {status}")
    return jsonify(status), 200


@main.route("/dict/available-lang")
def dict_available_languages() -> Tuple[Response, int]:
    available_lang = persistence_service.get_available_languages()
    app_log.debug(f"user queries available languages: {available_lang}")
    return jsonify(InfoRequestAvailDictLang(available_lang)), 200


@main.route("/dict/default-lang")
def dict_default_languages() -> Tuple[Response, int]:
    default_lang = persistence_service.get_default_languages()
    app_log.debug(f"user queries default languages: {default_lang}")
    return jsonify(InfoRequestAvailDictLang(default_lang)), 200


@main.route("/dict/lookup-option", methods=['POST'])
def lookup_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    dict_request = DictRequest(**request_data)
    app_log.debug(f"dict request: {dict_request}")
    dict_options_response: List[DictOptionsItem] = controller.lookup_dict_word(dict_request)

    output = [dataclasses.asdict(curr_option) for curr_option in dict_options_response]
    app_log.debug(f"response options: {output}")
    json: Response = jsonify(output)
    app_log.debug('lookup response json: %s', json.get_json())
    return json, 200


@main.route("/dict/select-option", methods=['POST'])
def select_word_options() -> Tuple[Response, int]:
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    selected_item_id: int = OptionSelectRequest(**request_data).selected_dict_options_item_id

    output = {
        'select_successful': controller.select_dict_word(selected_item_id)
    }

    app_log.debug(f"json output: {output}")
    return jsonify(output), 200
