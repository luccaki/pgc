from flask import Blueprint
import requests

master_route = Blueprint('master_route', __name__)

@master_route.route("/api/v1/teste", methods=['GET'])
def teste():
    return "teste"

@master_route.route("/api/v1/teste/s3", methods=['GET'])
def teste_s3():
    url = 'http://app_s3:3002/s3/api/v1/teste'
    response = requests.get(url)
    response.raise_for_status()
    return response.text