import sqlite3
import time
import requests
import json
import os
from dto.store_dto import StoreDto
from alive_progress import alive_bar
from view.view import View
from repository.store_repository import StoreRepository


class StoreParser:
    _url: str = ''
    _repository: StoreRepository = None

    def __init__(self):
        self._url = '%s/stores' % os.getenv('SOURCE_URL')
        self._repository = StoreRepository()

    def run(self) -> None:
        store_list = self._send_request()
        stores_dto = self._prepare_response(store_list)
        self._save_stores(stores_dto)

    def _send_request(self) -> list:
        response = requests.get(self._url)
        store_list = response.json()
        if not isinstance(store_list, list):
            raise RuntimeError('The endpoint of Stores returned incorrect data format!')

        return store_list

    @staticmethod
    def _prepare_response(resp_store_list: list) -> list[StoreDto]:
        stores: list[StoreDto] = []
        count: int = len(resp_store_list)
        print('\t%sFound stores: %s%d%s' % (View.COLOR_YELLOW, View.COLOR_RED, count, View.COLOR_DEFAULT))

        with alive_bar(count) as bar:
            print('\t%sParsing...%s' % (View.COLOR_YELLOW, View.COLOR_DEFAULT))
            for store in resp_store_list:
                stores.append(StoreDto(
                    id=int(store['id']),
                    name=str(store['name']),
                    source=json.dumps(store)
                ))
                time.sleep(0.01)
                bar()

        return stores

    def _save_stores(self, store_list: list[StoreDto]) -> None:
        with alive_bar(len(store_list)) as bar:
            print('\t%sSaving...%s' % (View.COLOR_YELLOW, View.COLOR_DEFAULT))
            for store in store_list:
                try:
                    self._repository.save(store)
                except (sqlite3.OperationalError, sqlite3.IntegrityError) as message:
                    print('\t%s%s (%s%d%s)%s Error: %s%s' % (
                        View.COLOR_BLUE,
                        store.name,
                        View.COLOR_L_BLUE,
                        store.id,
                        View.COLOR_BLUE,
                        View.COLOR_RED,
                        message,
                        View.COLOR_DEFAULT
                    ))
                time.sleep(0.01)
                bar()
