from scrap.product import Product


class ProductsController:
    def __init__(self, products: list[Product]):
        self.products = products

    @property
    def get_amount_of_products(self) -> int:
        return len(self.products)

    @property
    def calculate_average_price(self) -> float:
        total_price = 0
        for product in self.products:
            total_price += product.price
        return total_price / len(self.products)

    @property
    def find_highest_rated_sites_products(self) -> list[Product]:
        top_products = sorted(self.products, key=lambda product: product.store_rating, reverse=True)[:3]
        return top_products
    @property
    def find_lowest_price_product_with_highest_rated_site(self) -> Product:
        highest_rating_products = self.find_highest_rated_sites_products

        lowest_price_product = None

        for product in highest_rating_products:
            if lowest_price_product is None or product.price < lowest_price_product.price:
                lowest_price_product = product

        return lowest_price_product



