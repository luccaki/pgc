from flask import Flask
from flask_cors import CORS
from api.master import master_route
from utils.limiter import limiter

app = Flask(__name__)
limiter.init_app(app)
app.register_blueprint(master_route)

CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3001,debug=True,threaded=True)