from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
import json

# Path to a very large file you want to upload
FILE_PATH = "/home/luccaki/Desktop/pgc/image.jpeg"

driver = get_driver(Provider.GOOGLE_DRIVE)

container = driver.get_container('credentials.json')

extra = {"content_type": "image/jpeg"}

driver.upload_object(file_path='image.jpeg', container=container,extra=extra,object_name='image.jpeg')

obj = driver.get_object(container=container, object_name='image.jpeg')
print(obj)
driver.download_object(obj=obj,destination_path='/home/luccaki/Desktop/pgc/')

driver.delete_object(obj=obj)