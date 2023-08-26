from database.connector import Connector
from dto.product_dto import ProductDto
from dto.statistic_dto import StatisticDto
from repository.statistic_status import StatisticStatus
from database.model.product_model import Product
from database.model.statistic_model import Statistic


class ProductRepository(Connector):
    def save(self, product_dto: ProductDto, statistic_dto: StatisticDto) -> None:
        db = Connector.get_connection()
        with db.transaction() as transaction:
            Product.create(
                ean=product_dto.ean,
                store_id=product_dto.store_id,
                energy=product_dto.energy,
                protein=product_dto.protein,
                fat=product_dto.fat,
                carbohydrates=product_dto.carbohydrates,
                source=product_dto.source
            )
            Statistic.replace(
                store_id=statistic_dto.store_id,
                category_id=statistic_dto.category_id,
                last_product_ean=statistic_dto.last_product_ean,
                num_paginator_page=statistic_dto.num_paginator_page,
                status=StatisticStatus.IN_PROGRESS.value
            ).execute()
            
            transaction.commit()
