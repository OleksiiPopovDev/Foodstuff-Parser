import sqlite3
import time
import json
import os
from dto.category_dto import CategoryDto
from alive_progress import alive_bar
from repository.store_repository import StoreRepository
from repository.category_repository import CategoryRepository
from service.base_parser import BaseParser
from view.view import View


class CategoryParser(BaseParser):
    def __init__(self):
        self._store_repository = StoreRepository()
        self._category_repository = CategoryRepository()

    def run(self):
        stores = self._store_repository.list()

        for store in stores:
            url = '%s/stores/%s/categories' % (os.getenv('SOURCE_URL'), store.id)
            category_list = self.send_request(url)
            categories = self._prepare_response(category_list, store.id)
            exit()
            # self._save_stores(stores_dto)

    @staticmethod
    def _prepare_response(resp_category_list: list, store_id: int) -> list[CategoryDto]:
        stores: list[CategoryDto] = []
        count: int = len(resp_category_list)
        print('\t%sFound stores: %s%d%s' % (View.COLOR_YELLOW, View.COLOR_RED, count, View.COLOR_DEFAULT))

        with alive_bar(count) as bar:
            print('\t%sParsing...%s' % (View.COLOR_YELLOW, View.COLOR_DEFAULT))
            for category in resp_category_list:
                stores.append(CategoryDto(
                    id=category['id'],
                    store_id=store_id,
                    product_count=int(category['count']),
                    source=json.dumps(category)
                ))
                time.sleep(0.01)
                bar()

        return stores
