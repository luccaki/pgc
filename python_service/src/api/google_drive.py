import io
from flask import Blueprint, request, Response, send_file
from libcloud.storage.types import Provider, ObjectDoesNotExistError
from libcloud.storage.providers import get_driver

google_drive_route = Blueprint('google_drive_route', __name__)

@google_drive_route.route("/googledrive/v1/teste", methods=['GET'])
def teste():
    try:
        return f'teste GOOGLE DRIVE'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@google_drive_route.route("/googledrive/v1/file", methods=['POST'])
def post_file():
    try:
        file = request.files['file']
        credentials_key = {}
        driver = get_driver(Provider.GOOGLE_DRIVE)
        container = driver.get_container(credentials_key)
        extra = {"content_type": "application/octet-stream"}
        ret = driver.upload_object_via_stream(iterator=io.BytesIO(file.read()), container=container,extra=extra,object_name=file.filename)
        return f'Uploaded file: {ret}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500
    
@google_drive_route.route("/googledrive/v1/file", methods=['GET'])
def get_files():
    try:
        credentials_key = {}
        driver = get_driver(Provider.GOOGLE_DRIVE)
        container = driver.get_container(credentials_key)
        results = container.files().list().execute()
        files = results.get('files', [])
        return f'Found files: {list(files)}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@google_drive_route.route("/googledrive/v1/file/<file_name>", methods=['GET'])
def get_file(file_name):
    try:
        credentials_key = {}
        driver = get_driver(Provider.GOOGLE_DRIVE)
        container = driver.get_container(credentials_key)
        obj = driver.get_object(container=container, object_name=file_name)
        file_stream = driver.download_object_as_stream(obj)
        file_stream.seek(0)
        response = Response(file_stream, content_type="application/octet-stream")
        response.headers.set('Content-Disposition', 'attachment', filename=file_name)
        return response
    except ObjectDoesNotExistError:
        return f'File not found: {file_name}', 404
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@google_drive_route.route("/googledrive/v1/file/<container_name>/<file_name>", methods=['DELETE'])
def delete_file(container_name, file_name):
    try:
        access_key = request.headers.get('Access-Key')
        secret_key = request.headers.get('Secret-Key')
        cls = get_driver(Provider.S3)
        driver = cls(access_key, secret_key)
        container = driver.get_container(container_name=container_name)
        obj = driver.get_object(container_name=container.name, object_name=file_name)
        driver.delete_object(obj)
        return f'Deleted file: {file_name}'
    except ObjectDoesNotExistError:
        return f'File not found: {file_name}', 404
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500