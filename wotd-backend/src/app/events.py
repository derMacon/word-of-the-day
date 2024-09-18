import json
from typing import List

from flask import request
from flask_socketio import SocketIO

from src.controller.web_controller import WebController
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
    dict_request = DictRequest(**json_input)
    app_log.debug(f"socket request: {dict_request}")

    recommendations: List[str] = WebController().autocomplete_dict_word(dict_request)
    app_log.debug(f"lst_str output: {recommendations}")

    try:
        socketio.emit('update_autocorrect', recommendations, room=request.sid)
        socketio.stop()
    except Exception as e:
        app_log.error(f"Error sending image: {e}")
