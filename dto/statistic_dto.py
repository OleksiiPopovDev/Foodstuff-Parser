from repository.statistic_status import StatisticStatus


class StatisticDto:
    def __init__(
            self,
            store_id: int,
            category_id: str,
            last_product_ean: str = None,
            num_paginator_page: int = None,
            status: str = StatisticStatus.IN_PROGRESS.value
    ) -> None:
        self.store_id = store_id
        self.category_id = category_id
        self.last_product_ean = last_product_ean
        self.num_paginator_page = num_paginator_page
        self.status = status
