from locust import HttpUser, task
from requests_toolbelt import MultipartEncoder

idle_users = {id for id in range(1, 65535)}
provider = 'googledrive'
file_path = 'test_image.jpeg'

class TestUser(HttpUser):
    __user: int = None

    @task
    def TestHost(self):
        global provider
        global file_path
        file_name = f"{self.__user}_{file_path}"

        with open(file_path, 'rb') as file:
            file_content = file.read()

        multipart_data = MultipartEncoder(fields={'file': (file_name, file_content)})
        headers = {'Content-Type': multipart_data.content_type}

        self.client.post(f"/api/v1/{provider}/file", data=multipart_data, headers=headers, name="/post/file")
        self.client.get(f"/api/v1/{provider}/file/{file_name}", name="/get/file")

    def on_start(self):
        global idle_users
        self.__user = idle_users.pop()

    def on_stop(self):
        global provider
        global file_path
        file_name = f"{self.__user}_{file_path}"
        self.client.delete(f"/api/v1/{provider}/file/{file_name}", name="/delete/file")
        global idle_users
        idle_users.add(self.__user)