from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
import json

with open("aws_credentials.json", "r") as f:
    credentials = json.load(f)

# Path to a very large file you want to upload
FILE_PATH = "/home/luccaki/Desktop/pgc/image.jpeg"

cls = get_driver(Provider.S3)
driver = cls(credentials["access_key"], credentials["secret_key"])

container = driver.get_container(container_name="pgc-luccaki")


#extra = {"content_type": "application/octet-stream", "acl": "public-read"}

#with open(FILE_PATH, "rb") as iterator:
#    obj = driver.upload_object_via_stream(
#        iterator=iterator, container=container, object_name="teste.jpeg", extra=extra
#    )


objects = driver.list_container_objects(container)
print(objects)
obj = driver.get_object(container_name=container.name, object_name='test.jpeg')
driver.download_object(obj,'/home/luccaki/Desktop/pgc/')

driver.delete_object(obj)