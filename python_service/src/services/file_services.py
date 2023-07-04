import requests
from flask import Response
from utils.credentials import get_s3_credentials, get_google_credentials
import pybreaker

post_service_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=60)

#@post_service_breaker
def post_file_service(provider, file):
    if(provider == 's3'):
        credentials = get_s3_credentials()
        url = 'http://app_s3:3002/s3/v1/file/pgc-luccaki'
        headers = {
            'Access-Key': credentials['access_key'],
            'Secret-Key': credentials['secret_key']
        }
    elif(provider == 'googledrive'):
        credentials = get_google_credentials()
        url = 'http://app_google_drive:3003/googledrive/v1/file'
        headers = {
            'Project-Id': credentials['project_id'],
            'Private-Key-Id': credentials['private_key_id'],
            'Private-Key': credentials['private_key'],
            'Client-Email': credentials['client_email'],
            'Client-Id': credentials['client_id'],
            'Client-X509-Cert-Url': credentials['client_x509_cert_url']
        }
    elif(provider == 'ipfs'):
        url = 'http://app_ipfs:3004/ipfs/v1/file'
        headers = {}
    else:
        return Response(f'Wrong provider specified! ({provider})', 400)
    
    files = {'file': (file.filename, file)}
    response = requests.post(url, headers=headers, files=files)
    return Response(response, response.status_code)

def get_file_service(provider, file_name):
    if(provider == 's3'):
        credentials = get_s3_credentials()
        url = f'http://app_s3:3002/s3/v1/file/pgc-luccaki/{file_name}'
        headers = {
            'Access-Key': credentials['access_key'],
            'Secret-Key': credentials['secret_key']
        }
    elif(provider == 'googledrive'):
        credentials = get_google_credentials()
        url = f'http://app_google_drive:3003/googledrive/v1/file/{file_name}'
        headers = {
            'Project-Id': credentials['project_id'],
            'Private-Key-Id': credentials['private_key_id'],
            'Private-Key': credentials['private_key'],
            'Client-Email': credentials['client_email'],
            'Client-Id': credentials['client_id'],
            'Client-X509-Cert-Url': credentials['client_x509_cert_url']
        }
    elif(provider == 'ipfs'):
        url = f'http://app_ipfs:3004/ipfs/v1/file/{file_name}'
        headers = {}
    else:
        return Response(f'Wrong provider specified! ({provider})', 400)
    
    res = requests.get(url, headers=headers)
    response = Response(res, res.status_code, content_type="application/octet-stream")
    filename = res.headers.get('Content-Disposition').split("; ")[1].replace("filename=","").strip()
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response

def delete_file_service(provider, file_name):
    if(provider == 's3'):
        credentials = get_s3_credentials()
        url = f'http://app_s3:3002/s3/v1/file/pgc-luccaki/{file_name}'
        headers = {
            'Access-Key': credentials['access_key'],
            'Secret-Key': credentials['secret_key']
        }
    elif(provider == 'googledrive'):
        credentials = get_google_credentials()
        url = f'http://app_google_drive:3003/googledrive/v1/file/{file_name}'
        headers = {
            'Project-Id': credentials['project_id'],
            'Private-Key-Id': credentials['private_key_id'],
            'Private-Key': credentials['private_key'],
            'Client-Email': credentials['client_email'],
            'Client-Id': credentials['client_id'],
            'Client-X509-Cert-Url': credentials['client_x509_cert_url']
        }
    elif(provider == 'ipfs'):
        return Response(f'Can\'t delete from IPFS!', 400)
    else:
        return Response(f'Wrong provider specified! ({provider})', 400)
    
    response = requests.delete(url, headers=headers)
    return Response(response, response.status_code)