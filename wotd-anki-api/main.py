from flask import Flask

from src.app.routes import main

app = Flask(__name__)
app.debug = False
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
