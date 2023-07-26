from database.connector import Connector
from dto.store_dto import StoreDto


class StoreRepository(Connector):
    def save(self, store_dto: StoreDto) -> None:
        self.get_cursor().execute(
            "INSERT INTO store (id, name, source) VALUES (?, ?, ?)",
            (store_dto.id, store_dto.name, store_dto.source)
        )
        self.commit()
