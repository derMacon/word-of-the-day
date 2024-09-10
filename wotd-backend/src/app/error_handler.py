from flask import jsonify
from itsdangerous import BadSignature

from src.app import main
from src.data.error.anki_connect_error import AnkiConnectError
from src.data.error.anki_vnc_error import AnkiVncError
from src.data.error.missing_headers_error import MissingHeadersError
from src.utils.logging_config import app_log


@main.errorhandler(ValueError)
@main.errorhandler(TypeError)
@main.errorhandler(MissingHeadersError)
@main.errorhandler(AnkiVncError)
@main.errorhandler(AnkiConnectError)
def handle_value_error(error):
    app_log.error(f'http 400 - {error}')
    return jsonify({'type_error': f"invalid request: {error}"}), 400


@main.errorhandler(BadSignature)
def handle_signature_error(error):
    # TODO test this
    app_log.error(f'user tampered with signed uuid from cookie - {error}')
    return jsonify({'type_error': f"invalid request: {error}"}), 400

# TODO remove this handler function
# @main.errorhandler(AttributeError)
# @main.errorhandler(DatabaseError)
# def handle_attribute_error(error):
#     app_log.error(f'http 500 - {error}')
#     return jsonify({'database_error': f"internal server error: {error}"}), 500
