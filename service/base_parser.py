import requests


class BaseParser:
    @staticmethod
    def send_request(url: str) -> list:
        response = requests.get(url)
        data: object = response.json()
        if not isinstance(data, list):
            raise RuntimeError('The endpoint of Stores returned incorrect data format!')

        return data
