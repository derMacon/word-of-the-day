import json

from flask_socketio import SocketIO

from src.controller.web_controller import controller
from src.data.dict_input.dict_request import DictRequest
from src.utils.logging_config import app_log

socketio = SocketIO(cors_allowed_origins="*")


@socketio.on('connect')
def handle_connect():
    app_log.debug('Client connected')


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
        app_log.error(f"Error sending image: {e}")
