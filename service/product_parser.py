from service.base_parser import BaseParser
from repository.category_repository import CategoryRepository
from repository.product_repository import ProductRepository
from alive_progress import alive_bar
from view.view import View
from dto.product_dto import ProductDto
import json
import os
import time
import sqlite3


class ProductParser(BaseParser):

    def __init__(self):
        self._category_repository = CategoryRepository()
        self._product_repository = ProductRepository()

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
                    try:
                        product_list = data['results']
                        if len(product_list) == 0:
                            break
                        for product in product_list:
                            product_dto: ProductDto = ProductDto(
                                product['ean'],
                                category.store_id,
                                product['nutrition_facts']['ingredient_energy'],
                                product['nutrition_facts']['ingredient_protein'],
                                product['nutrition_facts']['ingredient_fat'],
                                product['nutrition_facts']['ingredient_carbohydrates'],
                                json.dumps(product)
                            )
                            self._product_repository.save(product_dto)
                            time.sleep(0.01)
                            bar()
                        page_num += 1
                        time.sleep(0.5)

                    except (KeyError, sqlite3.OperationalError, sqlite3.IntegrityError) as message:
                        print(
                            View.paint('\t{Blue}%d ({BBlue}%s{Blue}){Red} Error: Key %s not found!{ColorOff}') % (
                                category.store_id, category.id, message
                            )
                        )
