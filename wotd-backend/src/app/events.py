from flask_socketio import SocketIO

from src.utils.logging_config import app_log

socketio = SocketIO(cors_allowed_origins="*")


def test_socket_io():
    app_log.debug('testtest')
