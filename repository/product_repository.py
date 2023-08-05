from database.connector import Connector
from dto.product_dto import ProductDto
from dto.statistic_dto import StatisticDto
from repository.statistic_status import StatisticStatus


class ProductRepository(Connector):
    def save(self, product_dto: ProductDto, statistic_dto: StatisticDto) -> None:
        self.get_cursor().execute(
            "INSERT INTO product (ean, store_id, energy, protein, fat, carbohydrates, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                product_dto.ean,
                product_dto.store_id,
                product_dto.energy,
                product_dto.protein,
                product_dto.fat,
                product_dto.carbohydrates,
                product_dto.source
            )
        )
        self.get_cursor().execute(
            "INSERT OR REPLACE INTO statistic (store_id, category_id, last_product_ean, num_paginator_page, status) VALUES (?, ?, ?, ?, ?)",
            (
                statistic_dto.store_id,
                statistic_dto.category_id,
                statistic_dto.last_product_ean,
                statistic_dto.num_paginator_page,
                StatisticStatus.IN_PROGRESS.value
            )
        )
        self.commit()
