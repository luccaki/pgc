from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
import json

# Path to a very large file you want to upload
FILE_PATH = "/home/luccaki/Desktop/pgc/image.jpeg"

driver = get_driver(Provider.GOOGLE_DRIVE)

container = driver.get_container('credentials.json')

extra = {"content_type": "image/jpeg"}
file = open('image.jpeg', 'rb')
driver.upload_object_via_stream(iterator=file, container=container,extra=extra,object_name='image.jpeg')

obj = driver.get_object(container=container, object_name='image.jpeg')
print(obj)
file_stream = driver.download_object_as_stream(obj)

from PIL import Image
import io
image = Image.open(file_stream)
image.show()

#driver.delete_object(obj=obj)