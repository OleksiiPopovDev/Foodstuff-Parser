from database.connector import Connector
from dto.statistic_dto import StatisticDto


class StatisticRepository(Connector):
    def set_status(self, statistic_dto: StatisticDto):
        self.get_cursor().execute(
            "UPDATE statistic SET status = ? WHERE store_id = ? AND category_id = ?",
            (
                statistic_dto.status,
                statistic_dto.store_id,
                statistic_dto.category_id
            )
        )
        self.commit()
