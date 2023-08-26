class CategoryDto:
    def __init__(self, page: str, store_id: int, product_count: int, source: str) -> None:
        self.page = page
        self.store_id = store_id
        self.product_count = product_count
        self.source = source
