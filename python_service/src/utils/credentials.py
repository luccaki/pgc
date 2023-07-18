from dotenv import load_dotenv
import os

def get_s3_header():
    load_dotenv()
    return {
        'Access-Key': os.getenv("AWS_ACCESS_KEY"),
        'Secret-Key': os.getenv("AWS_SECRET_KEY")
    }

def get_google_header():
    load_dotenv()
    return {
        'Project-Id': os.getenv("GCP_PROJECT_ID"),
        'Private-Key-Id': os.getenv("GCP_PRIVATE_KEY_ID"),
        'Private-Key': os.getenv("GCP_PRIVATE_KEY"),
        'Client-Email': os.getenv("GCP_CLIENT_EMAIL"),
        'Client-Id': os.getenv("GCP_CLIENT_ID"),
        'Client-X509-Cert-Url': os.getenv("GCP_CLIENT_X509_CERT_URL")
    }

def get_credentials_from_header_google_drive(request):
    private_key = request.headers.get('Private-Key')
    return {
        "type": "service_account",
        "project_id": request.headers.get('Project-Id'),
        "private_key_id": request.headers.get('Private-Key-Id'),
        "private_key": eval(f'"{private_key}"'),
        "client_email": request.headers.get('Client-Email'),
        "client_id": request.headers.get('Client-Id'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": request.headers.get('Client-X509-Cert-Url')
    }

def get_credentials_from_header_s3(request):
    access_key = request.headers.get('Access-Key')
    secret_key = request.headers.get('Secret-Key')
    return access_key, secret_key