import io
from utils.credentials import get_credentials_from_header_google_drive
from flask import Blueprint, request, Response, send_file
from libcloud.storage.types import Provider, ObjectDoesNotExistError
from libcloud.storage.providers import get_driver

google_drive_route = Blueprint('google_drive_route', __name__)

@google_drive_route.route("/googledrive/v1/file", methods=['POST'])
def post_file():
    try:
        file = request.files['file']
        credentilas = get_credentials_from_header_google_drive(request)
        driver = get_driver(Provider.GOOGLE_DRIVE)
        container = driver.get_container(credentilas)
        extra = {"content_type": "application/octet-stream"}
        driver.upload_object_via_stream(iterator=io.BytesIO(file.read()), container=container,extra=extra,object_name=file.filename)
        return f'Uploaded file: {file.filename}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500
    
@google_drive_route.route("/googledrive/v1/file", methods=['GET'])
def get_files():
    try:
        credentilas = get_credentials_from_header_google_drive(request)
        driver = get_driver(Provider.GOOGLE_DRIVE)
        container = driver.get_container(credentilas)
        results = container.files().list().execute()
        files = map(lambda x: x['name'], results.get('files', []))
        return f'Found files: {list(files)}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@google_drive_route.route("/googledrive/v1/file/<file_name>", methods=['GET'])
def get_file(file_name):
    try:
        credentilas = get_credentials_from_header_google_drive(request)
        driver = get_driver(Provider.GOOGLE_DRIVE)
        container = driver.get_container(credentilas)
        obj = driver.get_object(container=container, object_name=file_name)
        file_stream = driver.download_object_as_stream(obj)
        response = Response(file_stream, content_type="application/octet-stream")
        response.headers.set('Content-Disposition', 'attachment', filename=file_name)
        return response
    except ObjectDoesNotExistError:
        return f'File not found: {file_name}', 404
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@google_drive_route.route("/googledrive/v1/file/<file_name>", methods=['DELETE'])
def delete_file(file_name):
    try:
        credentilas = get_credentials_from_header_google_drive(request)
        driver = get_driver(Provider.GOOGLE_DRIVE)
        container = driver.get_container(credentilas)
        obj = driver.get_object(container=container, object_name=file_name)
        driver.delete_object(obj=obj)
        return f'Deleted file: {file_name}'
    except ObjectDoesNotExistError:
        return f'File not found: {file_name}', 404
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500