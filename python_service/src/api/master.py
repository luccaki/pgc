from flask import Blueprint, request
from services.file_services import *
import pybreaker
    
master_route = Blueprint('master_route', __name__)

@master_route.route("/api/v1/<provider>/file", methods=['POST'])
def post_file(provider):
    try:
        file = request.files['file']
        res = post_service(provider, file)
        return res
    except pybreaker.CircuitBreakerError:
        return f'System Unstable! Please retry again later!', 500