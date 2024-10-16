from flask import Blueprint
from flask import Flask
from flask_cors import CORS

# TODO clean this up
# import src.app.routes
# from .routes import main
# import src.app.routes

from gevent import monkey
monkey.patch_all()

main = Blueprint('main', __name__, url_prefix='/api/v1')

from . import error_handler

from .routes import main
from .events import socketio

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    CORS(app)
    app.debug = debug
    app.register_blueprint(main)

    socketio.init_app(app)
    return app
