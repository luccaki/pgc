from locust import HttpUser, task
from requests_toolbelt import MultipartEncoder
import time

idle_users = {id for id in range(1, 65535)}
provider = 'googledrive'
file_path = 'test_image.jpeg'

class TestUser(HttpUser):
    __user: int = None

    @task
    def TestHost(self):
        global provider
        global file_path
        #file_name = f"{self.__user}_{file_path}"
        file_name = file_path

        #with open(file_path, 'rb') as file:
        #    file_content = file.read()

        #multipart_data = MultipartEncoder(fields={'file': (file_name, file_content)})
        #headers = {'Content-Type': multipart_data.content_type, 'User-Key': str(self.__user)}

        try:
            #post_res = self.client.post(f"/api/v1/{provider}/file", data=multipart_data, headers=headers, name="/post/file")
            #if post_res.status_code != 429:
            #    post_res.raise_for_status()
            #else:
            #    time.sleep(60)
            get_res = self.client.get(f"/api/v1/{provider}/file/{file_name}", headers={'User-Key': str(self.__user)}, name="/get/file")
            if get_res.status_code != 429:
                get_res.raise_for_status()
            else:
                time.sleep(60)
            #delete_res = self.client.delete(f"/api/v1/{provider}/file/{file_name}", headers={'User-Key': str(self.__user)}, name="/delete/file")
            #if delete_res.status_code != 429:
            #    delete_res.raise_for_status()
            #else:
            #    time.sleep(60)
        except Exception as e:
            print("An error occurred:", e)
            print("Number of Users:", self.environment.runner.user_count)
            self.environment.runner.stop()
            

    def on_start(self):
        global idle_users
        self.__user = idle_users.pop()

    def on_stop(self):
        global idle_users
        idle_users.add(self.__user)