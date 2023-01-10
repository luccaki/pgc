from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

FILE_PATH = "/home/luccaki/Desktop/pgc/image.jpeg"

driver = get_driver(Provider.IPFS)
#driver = cls()

container = driver.get_container("/ip4/127.0.0.1/tcp/5001")

#res = container.add_json({"Teste": "teste?"})
#res = driver.upload_object(FILE_PATH,container)
#print(res)

res = driver.get_object(container,'QmQVhku8rWNC6MAtuZG1ic7Fxvt4mKutrTWwe1E4ZpXwhX')

from PIL import Image
import io
image = Image.open(io.BytesIO(res))
image.show()

#print(container.cat(res))