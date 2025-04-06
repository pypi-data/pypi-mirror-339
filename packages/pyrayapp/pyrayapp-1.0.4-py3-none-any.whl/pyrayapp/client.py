import requests

class Client:
    def __init__(self, host="127.0.0.1", port=23517):
        self.host = host
        self.port = port

    def set_host(self, host: str):
        self.host = host

    def set_port(self, port: int):
        self.port = port

    def send(self, data: dict):
        url = f"http://{self.host}:{self.port}"
        response = requests.post(url, json=data)
        print(response.text)
        response.raise_for_status()

    def lock_exists(self, lock_name: str) -> dict:
        url = f"http://{self.host}:{self.port}/locks/{lock_name}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
