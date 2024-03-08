from flask import Flask

from src.app.routes import main

app = Flask(__name__)
app.debug = False
app.register_blueprint(main)
