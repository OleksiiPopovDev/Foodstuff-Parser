from service.base_parser import BaseParser
from repository.category_repository import CategoryRepository
from repository.product_repository import ProductRepository
from repository.statistic_repository import StatisticRepository
from repository.statistic_status import StatisticStatus
from alive_progress import alive_bar
from view.view import View
from dto.product_dto import ProductDto
from dto.statistic_dto import StatisticDto
import json
import os
import time
import sqlite3


class ProductParser(BaseParser):
    _NUTRITION_INGREDIENT_ENERGY: str = 'ingredient_energy'
    _NUTRITION_INGREDIENT_PROTEIN: str = 'ingredient_protein'
    _NUTRITION_INGREDIENT_FAT: str = 'ingredient_fat'
    _NUTRITION_INGREDIENT_CARBOHYDRATES: str = 'ingredient_carbohydrates'

    def __init__(self):
        self._category_repository = CategoryRepository()
        self._product_repository = ProductRepository()
        self._statistic_repository = StatisticRepository()

    def run(self):
        categories = self._category_repository.list()

        mockup_str: str = View.paint('{Blue}[{BBlue}%d{Blue}] {Cyan}%s{ColorOff} ')
        category_name_list: list[str] = []
        for category in categories:
            category_name_list.append(mockup_str % (category.store_id, category.id))
        biggest_line: int = View.count_biggest_line(category_name_list)

        for category in categories:
            with alive_bar(category.product_count) as bar:
                page_num: int = 1
                while True:
                    title: str = mockup_str % (category.store_id, category.id)
                    spaces: int = View.get_count_spaces_for_line_up(title, biggest_line)
                    bar.title(title + ' ' * spaces)

                    url = '%s/stores/%d/categories/%s/products/?page=%d' % (
                        os.getenv('SOURCE_URL'), category.store_id, category.id, page_num
                    )
                    data = self.send_request_product(url)

                    product_list = data['results']
                    if len(product_list) == 0:
                        statistic_dto: StatisticDto = StatisticDto(
                            store_id=category.store_id,
                            category_id=category.id,
                            status=StatisticStatus.DONE.value
                        )
                        self._statistic_repository.set_status(statistic_dto)
                        break
                    for product in product_list:
                        try:
                            product_ean: str = product['ean']
                        except KeyError:
                            print(View.paint(
                                '\t{Blue}%d ({BBlue}%s{Blue}){Red} Error: ean of product not found!') % (
                                      category.store_id,
                                      category.id
                                  ))

                        product_dto: ProductDto = ProductDto(
                            product_ean,
                            category.store_id,
                            self._check_nutrition_facts(product, self._NUTRITION_INGREDIENT_ENERGY),
                            self._check_nutrition_facts(product, self._NUTRITION_INGREDIENT_PROTEIN),
                            self._check_nutrition_facts(product, self._NUTRITION_INGREDIENT_FAT),
                            self._check_nutrition_facts(product, self._NUTRITION_INGREDIENT_CARBOHYDRATES),
                            json.dumps(product)
                        )
                        statistic_dto: StatisticDto = StatisticDto(
                            category.store_id,
                            category.id,
                            product_ean,
                            page_num,
                            StatisticStatus.IN_PROGRESS.value
                        )
                        try:
                            self._product_repository.save(product_dto, statistic_dto)
                        except (sqlite3.OperationalError, sqlite3.IntegrityError) as message:
                            print(
                                View.paint(
                                    '\t{Blue}%d ({BBlue}%s{Blue}){Red} Error: %s {Yellow}[{Purple}ean=%s, store_id=%s{Yellow}]{ColorOff}') % (
                                    category.store_id,
                                    category.id,
                                    message,
                                    product['ean'],
                                    category.store_id
                                )
                            )
                        time.sleep(0.01)
                        bar()
                    page_num += 1
                    time.sleep(0.5)

    @staticmethod
    def _check_nutrition_facts(product: dict, item: str) -> str:
        try:
            return product['nutrition_facts'][item]
        except KeyError:
            return ''
