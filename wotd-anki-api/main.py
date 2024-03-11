from flask import Flask
import src.app

# from src.app.routes import main

app = src.app.create_app(debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
