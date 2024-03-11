from flask import jsonify

from src.app.routes import main
from src.types.error.unauthorized_access_error import UnauthorizedAccessError
from src.utils.logging_config import log


@main.errorhandler(UnauthorizedAccessError)
def handle_value_error(error):
    log.error('unauthorized access: ', error)
    return jsonify({'unauthorized_access_error': f"invalid access token: {error}"}), 401

# @main.errorhandler(ValueError)
# @main.errorhandler(TypeError)
# def handle_value_error(error):
#     return jsonify({'type_error': f"invalid request: {error}"}), 400
#
#
# @main.errorhandler(AttributeError)
# @main.errorhandler(DatabaseError)
# def handle_attribute_error(error):
#     return jsonify({'database_error': f"internal server error: {error}"}), 500
