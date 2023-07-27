from database.connector import Connector
from dto.store_dto import StoreDto


class StoreRepository(Connector):
    def save(self, store_dto: StoreDto) -> None:
        self.get_cursor().execute(
            "INSERT INTO store (id, name, source) VALUES (?, ?, ?)",
            (store_dto.id, store_dto.name, store_dto.source)
        )
        self.commit()

    def list(self) -> list[StoreDto]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM store ORDER BY id")
        data = cursor.fetchall()

        stores: list[StoreDto] = []
        for store in data:
            stores.append(StoreDto(
                id=int(store[0]),
                name=str(store[1]),
                source=store[2]
            ))

        return stores
