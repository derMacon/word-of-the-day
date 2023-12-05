import dataclasses

from flask import jsonify, Blueprint, request

import json
from types import SimpleNamespace

from src.data.types import translate_dict_request, DictResponseOption, DictRequest, Language
from src.logic.controller import controller
from src.utils.logging_config import app_log

# main = Blueprint('main', __name__, url_prefix='/api/v1')

from src.app import main


@main.route("/health")
def test_log():
    status = {'status': 'running'}
    app_log.debug(f"health: {status}")
    return jsonify(status), 200



# src: https://stackoverflow.com/questions/72013377/how-to-parse-a-json-object-into-a-python-dataclass-without-third-party-library
@main.route("/lookup-option", methods=['POST'])
def lookup_word_options():
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    dict_request = DictRequest(**request_data)
    dict_response_option: DictResponseOption = controller.lookup_word(dict_request)

    output = jsonify(dataclasses.asdict(dict_response_option))
    app_log.debug(f"response options: {output}")
    return output, 200

    # return 'all good', 200


# @main.route("/select-option", methods=['POST'])
# def lookup_word_options():
#     # TODO implement this
#     pass
