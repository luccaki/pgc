from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

FILE_PATH = "/home/luccaki/Desktop/pgc/image.jpeg"

driver = get_driver(Provider.GOOGLE_DRIVE)
#driver = cls()

container = driver.get_container("/ip4/127.0.0.1/tcp/5001")

#res = container.add_json({"Teste": "teste?"})
res = driver.upload_object(FILE_PATH,container)
print(res)

res = driver.get_object(container,'QmRACojSdFuqnyyfQZ9Zgiz6zrVCUX1JRkYZyvRGu1MCzG')

from PIL import Image
import io
image = Image.open(io.BytesIO(res))
image.show()

#print(container.cat(res))