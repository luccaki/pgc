from flask import Flask
from flask_cors import CORS
from api.google_drive import google_drive_route

app = Flask(__name__)
app.register_blueprint(google_drive_route)

CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3003,debug=True,threaded=True)