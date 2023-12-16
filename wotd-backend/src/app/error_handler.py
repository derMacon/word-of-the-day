from flask import jsonify

from src.app import main
from src.data.error.database_error import DatabaseError


@main.errorhandler(ValueError)
@main.errorhandler(TypeError)
def handle_value_error(error):
    return jsonify({'type_error': f"invalid request: {error}"}), 400


@main.errorhandler(AttributeError)
@main.errorhandler(DatabaseError)
def handle_attribute_error(error):
    return jsonify({'database_error': f"internal server error: {error}"}), 500
