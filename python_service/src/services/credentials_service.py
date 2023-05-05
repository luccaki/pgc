from dotenv import load_dotenv
import os

def get_s3_credentials():
    load_dotenv()
    return {
        'access_key': os.getenv("AWS_ACCESS_KEY"),
        'secret_key': os.getenv("AWS_SECRET_KEY")
    }

def get_google_credentials():
    load_dotenv()
    return {
        'project_id': os.getenv("GCP_PROJECT_ID"),
        'private_key_id': os.getenv("GCP_PRIVATE_KEY_ID"),
        'private_key': os.getenv("GCP_PRIVATE_KEY"),
        'client_email': os.getenv("GCP_CLIENT_EMAIL"),
        'client_id': os.getenv("GCP_CLIENT_ID"),
        'client_x509_cert_url': os.getenv("GCP_CLIENT_X509_CERT_URL")
    }