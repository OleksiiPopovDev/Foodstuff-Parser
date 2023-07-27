class CategoryDto:
    def __init__(self, id: str, store_id: int, product_count: int, source: str) -> None:
        self.id = id
        self.store_id = store_id
        self.product_count = product_count
        self.source = source
