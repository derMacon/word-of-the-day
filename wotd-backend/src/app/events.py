from flask_socketio import SocketIO

from src.utils.logging_config import app_log

socketio = SocketIO(cors_allowed_origins="*")


def test_socket_io():
    app_log.debug('testtest')
    try:
        socketio.emit('update_autocorrect', ['abc', 'def', 'ghi'])
        socketio.stop()
    except Exception as e:
        print(f"Error sending image: {e}")
