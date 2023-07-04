from locust import HttpUser, task
from requests_toolbelt import MultipartEncoder
import time


class TestUser(HttpUser):
    @task
    def TestHost(self):
        provider = 'googledrive'
        file_path = 'test_image.jpeg'
        timestamp = f"{time.time()}.jpeg"

        with open(file_path, 'rb') as file:
            file_content = file.read()

        multipart_data = MultipartEncoder(fields={'file': (timestamp, file_content)})
        headers = {'Content-Type': multipart_data.content_type}
        
        self.client.post(f"/api/v1/{provider}/file", data=multipart_data, headers=headers, name="/post/file")
        self.client.get(f"/api/v1/{provider}/file/{timestamp}", name="/get/file")
        self.client.delete(f"/api/v1/{provider}/file/{timestamp}", name="/delete/file")