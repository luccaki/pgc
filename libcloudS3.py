from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

# Path to a very large file you want to upload
FILE_PATH = "/home/luccaki/Desktop/pgc/image.jpeg"

cls = get_driver(Provider.S3)
driver = cls("", "")

container = driver.get_container(container_name="pgc-luccaki")

# This method blocks until all the parts have been uploaded.
extra = {"content_type": "application/octet-stream", "acl": "public-read"}

with open(FILE_PATH, "rb") as iterator:
    obj = driver.upload_object_via_stream(
        iterator=iterator, container=container, object_name="test.jpeg", extra=extra
    )