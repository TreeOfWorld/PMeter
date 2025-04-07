# 基于locust的一个demo
from locust import run_single_user
from locust import HttpUser, task, between, constant_throughput


class QuickstartUser(HttpUser):
    # wait_time = between(1, 2)
    wait_time = constant_throughput(1)
    host = "http://localhost:8080"

    def on_start(self):
        self.client.post("/hello", json={"username": "foo", "password": "bar"})

    @task
    def view_item(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")

    @task
    def hello_world(self):
        self.client.post("/hello")
        # self.client.get("/world")


if __name__ == '__main__':
    run_single_user(QuickstartUser)
