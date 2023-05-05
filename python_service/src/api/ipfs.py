from flask import Blueprint, request, Response
from libcloud.storage.types import Provider, ObjectDoesNotExistError
from libcloud.storage.providers import get_driver
#from utils.credentials import get_credentials_from_header_ipfs
import io
import json

ipfs_route = Blueprint('ipfs_route', __name__)

@ipfs_route.route("/ipfs/v1/teste", methods=['GET'])
def teste():
    try:
        return f'TESTE_IPFS'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@ipfs_route.route("/ipfs/v1/file", methods=['POST'])
def post_file():
    try:
        file = request.files['file']
        driver = get_driver(Provider.IPFS)
        container = driver.get_container("/ip4/172.27.0.2/tcp/5001")
        file_hash = driver.upload_object_via_stream(iterator=file, container=container)
        res = driver.upload_object(object={"FileName": file.filename, "FileHash": file_hash}, container=container)
        return f'Uploaded file: {res}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500
    
#@ipfs_route.route("/ipfs/v1/file/<container_name>", methods=['GET'])
#def get_files(container_name):
#    try:
#        access_key, secret_key = get_credentials_from_header_ipfs(request)
#        cls = get_driver(Provider.ipfs)
#        driver = cls(access_key, secret_key)
#        container = driver.get_container(container_name=container_name)
#        objects = driver.list_container_objects(container)
#        return f'Found files: {list(map(lambda x: x.name, objects))}'
#    except Exception as e:
#        return f'Internal ERROR: {str(e)}', 500#

@ipfs_route.route("/ipfs/v1/file/<hash>", methods=['GET'])
def get_file(hash):
    try:
        driver = get_driver(Provider.IPFS)
        container = driver.get_container("/ip4/172.27.0.2/tcp/5001")
        file = driver.get_object(container, hash)
        file_str = file.decode('utf-8')
        file_json = json.loads(file_str)
        file_name = file_json["FileName"]
        file_byte = driver.get_object(container, file_json["FileHash"])
        response = Response(file_byte, content_type="application/octet-stream")
        response.headers.set('Content-Disposition', 'attachment', filename=file_name)
        return response
    except ObjectDoesNotExistError:
        return f'File not found: {hash}', 404
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

#@ipfs_route.route("/ipfs/v1/file/<container_name>/<file_name>", methods=['DELETE'])
#def delete_file(container_name, file_name):
#    try:
#        access_key, secret_key = get_credentials_from_header_ipfs(request)
#        cls = get_driver(Provider.ipfs)
#        driver = cls(access_key, secret_key)
#        container = driver.get_container(container_name=container_name)
#        obj = driver.get_object(container_name=container.name, object_name=file_name)
#        driver.delete_object(obj)
#        return f'Deleted file: {file_name}'
#    except ObjectDoesNotExistError:
#        return f'File not found: {file_name}', 404
#    except Exception as e:
#        return f'Internal ERROR: {str(e)}', 500