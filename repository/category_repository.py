from database.connector import Connector
from dto.category_dto import CategoryDto


class CategoryRepository(Connector):
    def save(self, category_dto: CategoryDto) -> None:
        self.get_cursor().execute(
            "INSERT INTO category (id, store_id, product_count, source) VALUES (?, ?, ?, ?)",
            (category_dto.id, category_dto.store_id, category_dto.product_count, category_dto.source)
        )
        self.commit()
