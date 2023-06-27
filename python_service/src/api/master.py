from flask import Blueprint, request
from services.file_services import *
import pybreaker
from utils.limiter import limiter
import socket
master_route = Blueprint('master_route', __name__)

@master_route.route("/api/v1/<provider>/file", methods=['POST'])
@limiter.exempt
def post_file(provider):
    try:
        file = request.files['file']
        res = post_service(provider, file)
        return res
    except pybreaker.CircuitBreakerError:
        return f'System Unstable! Please retry again later!', 500
    
@master_route.route("/api/v1/<provider>/file/<file_name>", methods=['GET'])
@limiter.exempt
def get_file(provider, file_name):
    try:
        res = get_service(provider, file_name)
        return res
    except pybreaker.CircuitBreakerError:
        return f'System Unstable! Please retry again later!', 500

@master_route.route("/hostname", methods=['get'])
@limiter.exempt
def get_Free():
    return f'Hosname: {socket.gethostname()}', 200