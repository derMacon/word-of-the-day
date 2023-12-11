import dataclasses

from flask import jsonify, request

from src.app import main
from src.data.types import DictOptionsResponse, DictRequest, OptionSelectRequest
from src.logic.controller import controller
from src.utils.logging_config import app_log


@main.route("/health")
def test_log():
    status = {'status': 'running'}
    app_log.debug(f"health: {status}")
    return jsonify(status), 200


@main.route("/dict/lookup-option", methods=['POST'])
def lookup_word_options():
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    dict_request = DictRequest(**request_data)
    dict_response_option: DictOptionsResponse = controller.lookup_dict_word(dict_request)

    output = dataclasses.asdict(dict_response_option)
    app_log.debug(f"response options: {output}")
    return jsonify(output), 200



@main.route("/dict/select-option", methods=['POST'])
def select_word_options():
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    option_select_request = OptionSelectRequest(**request_data)

    output = jsonify({
        'select_successful': controller.select_dict_word(option_select_request)
    })

    app_log.debug(f"json output: {output}")
    return output, 200


