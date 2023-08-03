import sqlite3
import time
import json
import os
from dto.store_dto import StoreDto
from alive_progress import alive_bar
from view.view import View
from repository.store_repository import StoreRepository
from service.base_parser import BaseParser


class StoreParser(BaseParser):
    def __init__(self):
        self._url = '%s/stores' % os.getenv('SOURCE_URL')
        self._repository = StoreRepository()

    def run(self) -> None:
        store_list = self.send_request(self._url)
        stores = self._prepare_response(store_list)
        self._save_stores(stores)

    @staticmethod
    def _prepare_response(resp_store_list: list) -> list[StoreDto]:
        stores: list[StoreDto] = []
        count: int = len(resp_store_list)
        print(View.paint('\t{Yellow}Found stores: {Red}%d{ColorOff}' % count))

        with alive_bar(count) as bar:
            bar.title(View.paint('\t\t{Yellow}Parsing...{ColorOff}'))
            for store in resp_store_list:
                stores.append(StoreDto(
                    id=int(store['id']),
                    name=str(store['name']),
                    source=json.dumps(store)
                ))

                bar()
                time.sleep(0.01)

        return stores

    def _save_stores(self, store_list: list[StoreDto]) -> None:
        with alive_bar(len(store_list)) as bar:
            bar.title(View.paint('\t\t{Yellow}Saving... {ColorOff}'))
            for store in store_list:
                try:
                    self._repository.save(store)
                except (sqlite3.OperationalError, sqlite3.IntegrityError) as message:
                    print('\t{Blue}%s ({BBlue}%d{Blue}){Red} Error: %s{ColorOff}' % (store.name, store.id, message))

                bar()
                time.sleep(0.01)
