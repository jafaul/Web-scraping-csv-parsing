from typing import Any


class Product:
    def __init__(self, name: str, price: float, store_rating: float, website: str):
        self.name = name
        self.price = price
        self.store_rating = store_rating
        self.website = website

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "price": self.price,
            "store_rating": self.store_rating,
            "website": self.website
        }