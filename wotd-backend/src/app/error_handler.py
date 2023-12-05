from src.app import main
import dataclasses

from flask import jsonify, Blueprint, request

import json
from types import SimpleNamespace


@main.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({'type_error': f"invalid request: {error}"}), 400


@main.errorhandler(AttributeError)
def handle_attribute_error(error):
    return jsonify({'attribute_error': f"internal server error: {error}"}), 500
