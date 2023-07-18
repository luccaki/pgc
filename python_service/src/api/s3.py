from flask import Blueprint, request, Response
from libcloud.storage.types import Provider, ObjectDoesNotExistError
from libcloud.storage.providers import get_driver
from utils.credentials import get_credentials_from_header_s3

s3_route = Blueprint('s3_route', __name__)

@s3_route.route("/s3/v1/file/<container_name>", methods=['POST'])
def post_file(container_name):
    try:
        access_key, secret_key = get_credentials_from_header_s3(request)
        file = request.files['file']
        cls = get_driver(Provider.S3)
        driver = cls(access_key, secret_key)
        container = driver.get_container(container_name=container_name)
        extra = {"content_type": "application/octet-stream", "acl": "public-read"}
        obj = driver.upload_object_via_stream(iterator=file, container=container, object_name=file.filename, extra=extra)
        return f'Uploaded file: {obj.name}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500
    
@s3_route.route("/s3/v1/file/<container_name>", methods=['GET'])
def get_files(container_name):
    try:
        access_key, secret_key = get_credentials_from_header_s3(request)
        cls = get_driver(Provider.S3)
        driver = cls(access_key, secret_key)
        container = driver.get_container(container_name=container_name)
        objects = driver.list_container_objects(container)
        return f'Found files: {list(map(lambda x: x.name, objects))}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@s3_route.route("/s3/v1/file/<container_name>/<file_name>", methods=['GET'])
def get_file(container_name, file_name):
    try:
        access_key, secret_key = get_credentials_from_header_s3(request)
        cls = get_driver(Provider.S3)
        driver = cls(access_key, secret_key)
        container = driver.get_container(container_name)
        obj = driver.get_object(container_name=container.name, object_name=file_name)
        file_stream = driver.download_object_as_stream(obj)
        response = Response(file_stream, content_type="application/octet-stream")
        response.headers.set('Content-Disposition', 'attachment', filename=file_name)
        return response
    except ObjectDoesNotExistError:
        return f'File not found: {file_name}', 404
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@s3_route.route("/s3/v1/file/<container_name>/<file_name>", methods=['DELETE'])
def delete_file(container_name, file_name):
    try:
        access_key, secret_key = get_credentials_from_header_s3(request)
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