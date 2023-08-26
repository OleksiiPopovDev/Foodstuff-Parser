from database.connector import Connector
from dto.store_dto import StoreDto
from database.model.store_model import Store


class StoreRepository(Connector):
    @staticmethod
    def save(store_dto: StoreDto) -> None:
        Store.create(id=store_dto.id, name=store_dto.name, source=store_dto.source)

    @staticmethod
    def list() -> list[StoreDto]:
        data = Store.select().order_by(Store.id)

        stores: list[StoreDto] = []
        for store in data:
            stores.append(StoreDto(
                id=store.id,
                name=str(store.name),
                source=store.source
            ))

        return stores
