import sqlite3
import time
import json
import os
from dto.category_dto import CategoryDto
from dto.store_dto import StoreDto
from alive_progress import alive_bar
from repository.store_repository import StoreRepository
from repository.category_repository import CategoryRepository
from service.base_parser import BaseParser
from view.view import View


class CategoryParser(BaseParser):
    _biggest_name: int = 0
    def __init__(self):
        self._store_repository = StoreRepository()
        self._category_repository = CategoryRepository()

    def run(self):
        stores = self._store_repository.list()

        for store in stores:
            name_length = len(store.name)
            self._biggest_name = name_length if name_length > self._biggest_name else self._biggest_name

        for store in stores:
            url = '%s/stores/%s/categories' % (os.getenv('SOURCE_URL'), store.id)
            category_list = self.send_request(url)
            categories = self._prepare_response(category_list, store)
            self._save_categories(store, categories)

    def _save_categories(self, store: StoreDto, categories: list[CategoryDto]) -> None:
        categories_count: int = len(categories)
        with alive_bar(categories_count) as bar:
            more_spaces: int = self._biggest_name - len(store.name)
            bar.title('[%s%s%s] %sFound categories: %s%d%s ' % (
                View.COLOR_CYAN,
                store.name,
                View.COLOR_DEFAULT,
                View.COLOR_YELLOW,
                View.COLOR_RED,
                categories_count,
                View.COLOR_DEFAULT
            ) + " " * more_spaces)

            for category in categories:
                try:
                    self._category_repository.save(category)
                except (sqlite3.OperationalError, sqlite3.IntegrityError) as message:
                    print('%s%s %s Error: %s%s' % (
                        View.COLOR_BLUE,
                        category.id,
                        View.COLOR_RED,
                        message,
                        View.COLOR_DEFAULT
                    ))
                bar()

    @staticmethod
    def _prepare_response(resp_category_list: list, store: StoreDto) -> list[CategoryDto]:
        categories: list[CategoryDto] = []
        for category in resp_category_list:
            categories.append(CategoryDto(
                id=category['id'],
                store_id=store.id,
                product_count=int(category['count']),
                source=json.dumps(category)
            ))

        return categories
