from flask import Blueprint, request, Response
from utils.credentials import *
from utils.limiter import limiter
import pybreaker
import requests
import socket

master_route = Blueprint('master_route', __name__)

post_service_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=60)

def get_user_identifier():
    return request.headers.get('User-Key')

#@post_service_breaker
@master_route.route("/api/v1/<provider>/file", methods=['POST'])
@limiter.limit("3 per minute", key_func=get_user_identifier)
def post_file(provider):
    try:
        file = request.files['file']
        if(provider == 's3'):
            url = 'http://nginx/s3/v1/file/pgc-luccaki'
            headers = get_s3_header()
        elif(provider == 'googledrive'):
            url = 'http://nginx/googledrive/v1/file'
            headers = get_google_header()
        elif(provider == 'ipfs'):
            url = 'http://nginx/ipfs/v1/file'
            headers = {}
        else:
            raise ValueError(f'Wrong provider specified! ({provider})')

        files = {'file': (file.filename, file)}
        res = requests.post(url, headers=headers, files=files)
        return Response(res.content, status=res.status_code, headers=dict(res.headers))
    except pybreaker.CircuitBreakerError:
        return f'System Unstable! Please retry again later!', 500
    except ValueError as e:
        return f'Bad Request? {str(e)}', 400
    except Exception as e:
        return f'An error occurred: {str(e)}', 500
    
@master_route.route("/api/v1/<provider>/file/<file_name>", methods=['GET'])
#@limiter.limit("3 per minute", key_func=get_user_identifier)
@limiter.exempt()
def get_file(provider, file_name):
    try:
        if(provider == 's3'):
            url = f'http://nginx/s3/v1/file/pgc-luccaki/{file_name}'
            headers = get_s3_header()
        elif(provider == 'googledrive'):
            url = f'http://app_google_drive:3003/googledrive/v1/file/{file_name}'
            headers = get_google_header()
        elif(provider == 'ipfs'):
            url = f'http://nginx/ipfs/v1/file/{file_name}'
            headers = {}
        else:
            raise ValueError(f'Wrong provider specified! ({provider})')
        
        res = requests.get(url, headers=headers)
        return Response(res, status=res.status_code, headers=dict(res.headers))
    except pybreaker.CircuitBreakerError:
        return f'System Unstable! Please retry again later!', 500
    except ValueError as e:
        return f'Bad Request? {str(e)}', 400
    except Exception as e:
        return f'An error occurred: {str(e)}', 500
    
@master_route.route("/api/v1/<provider>/file/<file_name>", methods=['DELETE'])
@limiter.limit("3 per minute", key_func=get_user_identifier)
def delete_file(provider, file_name):
    try:
        if(provider == 's3'):
            url = f'http://nginx/s3/v1/file/pgc-luccaki/{file_name}'
            headers = get_s3_header()
        elif(provider == 'googledrive'):
            url = f'http://nginx/googledrive/v1/file/{file_name}'
            headers = get_google_header()
        elif(provider == 'ipfs'):
            raise ValueError(f'Can\'t delete from IPFS!')
        else:
            raise ValueError(f'Wrong provider specified! ({provider})')

        res = requests.delete(url, headers=headers)
        return Response(res.content, status=res.status_code, headers=dict(res.headers))
    except pybreaker.CircuitBreakerError:
        return f'System Unstable! Please retry again later!', 500
    except ValueError as e:
        return f'Bad Request? {str(e)}', 400
    except Exception as e:
        return f'An error occurred: {str(e)}', 500

@master_route.route("/hostname", methods=['get'])
@limiter.exempt
def get_Free():
    return f'Hosname: {socket.gethostname()}', 200