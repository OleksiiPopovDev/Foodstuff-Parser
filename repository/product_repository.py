from database.connector import Connector
from dto.product_dto import ProductDto


class ProductRepository(Connector):
    def save(self, product_dto: ProductDto) -> None:
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
        self.commit()
