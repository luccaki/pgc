from flask import Flask, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

@app.route('/test')
def test():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=3001,debug=True,threaded=True)