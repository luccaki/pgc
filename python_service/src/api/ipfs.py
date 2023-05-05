from flask import Blueprint, request, Response
from libcloud.storage.types import Provider, ObjectDoesNotExistError
from libcloud.storage.providers import get_driver
import json

IP_IPFS_NODE = "/ip4/172.27.0.2/tcp/5001"

ipfs_route = Blueprint('ipfs_route', __name__)

@ipfs_route.route("/ipfs/v1/file", methods=['POST'])
def post_file():
    try:
        file = request.files['file']
        driver = get_driver(Provider.IPFS)
        container = driver.get_container(IP_IPFS_NODE)
        file_hash = driver.upload_object_via_stream(iterator=file, container=container)
        res = driver.upload_object(object={"FileName": file.filename, "FileHash": file_hash}, container=container)
        return f'Uploaded file: {res}'
    except Exception as e:
        return f'Internal ERROR: {str(e)}', 500

@ipfs_route.route("/ipfs/v1/file/<hash>", methods=['GET'])
def get_file(hash):
    try:
        driver = get_driver(Provider.IPFS)
        container = driver.get_container(IP_IPFS_NODE)
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