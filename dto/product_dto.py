class ProductDto:
    def __init__(
            self,
            ean: str,
            store_id: int,
            energy: str,
            protein: str,
            fat: str,
            carbohydrates: str,
            source: str
    ) -> None:
        self.ean = ean
        self.store_id = store_id
        self.energy = energy
        self.protein = protein
        self.fat = fat
        self.carbohydrates = carbohydrates
        self.source = source
