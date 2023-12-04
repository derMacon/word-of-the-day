from flask import Flask
from flask_cors import CORS

from .routes import main


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    CORS(app)
    app.debug = debug
    app.register_blueprint(main)

    return app
