import requests
from services.credentials_service import *

def post_service(provider, file):
    if(provider == 's3'):
        credentials = get_s3_credentials()
        url = 'http://app_s3:3002/s3/v1/file/pgc-luccaki'
        headers = {
            'Access-Key': credentials['access_key'],
            'Secret-Key': credentials['secret_key']
        }
        files = {'file': (file.filename, file)}
        response = requests.post(url, headers=headers, files=files)
        return response