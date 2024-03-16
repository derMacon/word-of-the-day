import threading

import src.app

app = src.app.create_app(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True) # TODO delete this
