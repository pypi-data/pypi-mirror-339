import requests

from ..api_abc import API_Requester


class BasicRequester(API_Requester):
    def request(self, method, url, serialized_data: dict) -> tuple[int, dict]:
        rps = requests.request(method, url, data=serialized_data)
        return rps.status_code, rps.json()
