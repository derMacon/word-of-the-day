from flask import Flask
from flask_cors import CORS

# import src.app.routes

# from .routes import main
# import src.app.routes

from flask import jsonify, Blueprint, request

main = Blueprint('main', __name__, url_prefix='/api/v1')

from . import routes
from . import error_handler


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    CORS(app)
    app.debug = debug
    app.register_blueprint(main)

    return app
