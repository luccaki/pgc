from flask import Flask
from flask_cors import CORS
from api.google_drive import google_drive_route
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import sys
from logging import StreamHandler

app = Flask(__name__)

stdout_handler = StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
app.logger.addHandler(stdout_handler)
#app.wsgi_app = ProxyFix(
#    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
#)
app.register_blueprint(google_drive_route)

CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3003)