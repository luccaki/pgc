from flask import Flask
from flask_cors import CORS
from api.s3 import s3_route

app = Flask(__name__)
app.register_blueprint(s3_route)

CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3002,debug=True,threaded=True)