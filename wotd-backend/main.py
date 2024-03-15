import threading

import src.app
from src.logic.housekeeping_controller import HousekeepingController

# from src.app import create_app

app = src.app.create_app(debug=True)
housekeeping_controller = HousekeepingController()

if __name__ == '__main__':
    threading.Thread(target=housekeeping_controller.run).start()
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True) # TODO delete this
