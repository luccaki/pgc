from locust import HttpUser, task
from requests_toolbelt import MultipartEncoder
import time
import locust.stats

locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 1

idle_users = {id for id in range(1, 999999)}
provider = 'googledrive'
file_path = 'test_image.jpeg'

class TestUser(HttpUser):
    __user: int = None
    @task
    def TestHost(self):
        global provider
        global file_path
        file_name = file_path
        self.client.get(f"/api/v1/{provider}/file/{file_name}", headers={'User-Key': str(self.__user)}, name="/get/file")
        time.sleep(9999999999999999999)

    def on_start(self):
        global idle_users
        self.__user = idle_users.pop()

    def on_stop(self):
        global idle_users
        idle_users.add(self.__user)