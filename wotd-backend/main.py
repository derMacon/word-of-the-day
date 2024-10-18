from gevent.pywsgi import WSGIServer

import src.app
from src.controller.cron_scheduler import configure_housekeeping_background_scheduler

app = src.app.create_app(debug=True)
configure_housekeeping_background_scheduler()

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    print("Server started on http://0.0.0.0:5000")
    http_server.serve_forever()
