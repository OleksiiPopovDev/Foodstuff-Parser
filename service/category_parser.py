import time
import json
import os
from peewee import IntegrityError
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
            url = os.getenv('SOURCE_CATEGORY_URL').replace('{STORE_ID}', str(store.id))
            category_list = self.send_request(url)
            categories = self.__prepare_response(category_list, store)
            self.__save_categories(store, categories)
            time.sleep(1)

    def __save_categories(self, store: StoreDto, categories: list[CategoryDto]) -> None:
        categories_count: int = len(categories)
        with alive_bar(categories_count) as bar:
            more_spaces: int = 30 - len(store.name)
            txt: str = View.paint('[{Cyan}%s{ColorOff}] %s{Yellow}Found categories: {Red}%d{ColorOff} ')
            bar.title(txt % (store.name, ' ' * more_spaces, categories_count))

            for category in categories:
                try:
                    self._category_repository.save(category)
                except IntegrityError as message:
                    txt: str = View.paint('{Blue}%s {Red} Error: %s{ColorOff}')
                    print(txt % (category.page, message))
                bar()

    @staticmethod
    def __prepare_response(resp_category_list: list, store: StoreDto) -> list[CategoryDto]:
        categories: list[CategoryDto] = []
        for category in resp_category_list:
            categories.append(CategoryDto(
                id=0,
                page=category['id'],
                store_id=store.id,
                product_count=int(category['count']),
                source=json.dumps(category)
            ))

        return categories
