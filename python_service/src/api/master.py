from flask import Blueprint, request, Response
from services.file_services import *

master_route = Blueprint('master_route', __name__)

@master_route.route("/api/v1/teste", methods=['GET'])
def teste():
    return "teste"

@master_route.route("/api/v1/<provider>/file", methods=['POST'])
def post_file(provider):
    file = request.files['file']
    res = post_service(provider, file)
    return Response(res, status=res.status_code )