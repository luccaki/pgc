from flask import Blueprint, request

master_route = Blueprint('master_route', __name__)

@master_route.route("/api/v1/teste", methods=['GET'])
def teste():
    return "teste"