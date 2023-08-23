import requests
from view.view import View
import time


class BaseParser:
    @staticmethod
    def send_request(url: str) -> list:
        response = requests.get(url)
        data: object = response.json()
        if not isinstance(data, list):
            raise RuntimeError('The endpoint of Stores returned incorrect data format!')

        return data

    @staticmethod
    def send_request_product(url: str) -> dict:
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as message:
            wait_seconds: int = 60
            print(
                View.paint(
                    '\t{Blue}({BBlue}Requester{Blue}){Red} Error: %s {Yellow}[{Purple}Waiting %d secends{Yellow}]{ColorOff}'
                ) % (message, wait_seconds)
            )
            time.sleep(wait_seconds)
            response = requests.get(url)

        data: dict = response.json()

        if not isinstance(data, dict):
            raise RuntimeError('The endpoint of Stores returned incorrect data format!')

        return data
