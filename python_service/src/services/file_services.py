import requests
from flask import Response
from utils.credentials import get_s3_credentials, get_google_credentials

def post_service(provider, file):
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
        return f'Wrong provider specified! ({provider})', 400
    
    files = {'file': (file.filename, file)}
    response = requests.post(url, headers=headers, files=files)
    return Response(response, response.status_code)