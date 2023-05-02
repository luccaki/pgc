from flask import Blueprint, request

s3_route = Blueprint('s3_route', __name__)

@s3_route.route("/s3/api/v1/teste", methods=['GET'])
def teste():
    return "teste_s3"