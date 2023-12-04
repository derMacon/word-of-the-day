from flask import jsonify, Blueprint, request

from src.data.types import translate_dict_request, DictResponseOption
from src.logic.controller import controller
from src.utils.logging_config import app_log

main = Blueprint('main', __name__, url_prefix='/api/v1')


@main.route("/health")
def test_log():
    status = {'status': 'running'}
    app_log.debug(f"health: {status}")
    return jsonify(status), 200


@main.route("/lookup-option", methods=['POST'])
def lookup_word_options():
    request_data = request.get_json()
    app_log.debug(f"request data: {request_data}")

    try:
        dict_request = translate_dict_request(request_data)
    except Exception as e:
        error = str(e)
        app_log.error(error)
        return jsonify({'error': error}), 400

    dict_response_option: DictResponseOption = controller.lookup_word(dict_request)

    app_log.debug(f"response options: {dict_response_option.to_map()}")

    return jsonify(dict_response_option.to_map()), 200


# @main.route("/select-option", methods=['POST'])
# def lookup_word_options():
#     # TODO implement this
#     pass
