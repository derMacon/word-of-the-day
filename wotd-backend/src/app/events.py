import json

from flask import jsonify
from flask_socketio import SocketIO

from src.controller.web_controller import controller
from src.data.dict_input.dict_request import DictRequest
from src.utils.logging_config import app_log

socketio = SocketIO(cors_allowed_origins="*")


def test_socket_io():
    app_log.debug('testtest')
    try:
        socketio.emit('update_autocorrect', ['abc', 'def', 'ghi'])
        socketio.stop()
    except Exception as e:
        print(f"Error sending image: {e}")
        
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('autocomplete-query-event')
def handle_autocomplete_query_event(request_data):
    app_log.debug('handle autocomplete query event: %s', request_data)
    json_input = json.loads(request_data)
    request = DictRequest(**json_input)
    app_log.debug(f"socket request: {request}")

    lst_str_output = controller.autocomplete_dict_word(request)
    app_log.debug(f"lst_str output: {lst_str_output}")

    try:
        socketio.emit('update_autocorrect', lst_str_output)
        socketio.stop()
    except Exception as e:
        print(f"Error sending image: {e}")
