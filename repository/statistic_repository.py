from database.connector import Connector
from dto.statistic_dto import StatisticDto
from repository.statistic_status import StatisticStatus
from database.model.statistic_model import Statistic


class StatisticRepository(Connector):
    @staticmethod
    def set_status(statistic_dto: StatisticDto):
        query = (
            Statistic
            .update(status=statistic_dto.status)
            .where(
                (Statistic.store == statistic_dto.store_id) & (Statistic.category == statistic_dto.category_id)
            )
        )

        query.execute()

    @staticmethod
    def get_in_progress() -> StatisticDto:
        try:
            data: Statistic = Statistic.get(Statistic.status == StatisticStatus.IN_PROGRESS.value)
        except Statistic.DoesNotExist:
            raise RuntimeError('Statistic is empty! Parse all')

        return StatisticDto(
            store_id=int(data.store.id),
            category_id=str(data.category_id),
            last_product_ean=str(data.last_product_ean),
            num_paginator_page=int(data.num_paginator_page),
            status=StatisticStatus.IN_PROGRESS.value
        )
