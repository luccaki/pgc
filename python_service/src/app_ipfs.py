from flask import Flask
from flask_cors import CORS
from api.ipfs import ipfs_route

app = Flask(__name__)
app.register_blueprint(ipfs_route)

CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3004,debug=True,threaded=True)