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
        print('\t%sFound stores: %s%d%s' % (View.COLOR_YELLOW, View.COLOR_RED, count, View.COLOR_DEFAULT))

        with alive_bar(count) as bar:
            bar.title('\t%sParsing...%s' % (View.COLOR_YELLOW, View.COLOR_DEFAULT))
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
            bar.title('\t%sSaving... %s' % (View.COLOR_YELLOW, View.COLOR_DEFAULT))
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
