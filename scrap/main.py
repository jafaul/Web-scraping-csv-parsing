import asyncio
import time
from pprint import pprint

from scrap.config import BASE_URL
from scrap.products_controller import ProductsController
from scrap.page_extractor import PageExtractor


async def main():
    start_time = time.perf_counter()

    page_extractor = PageExtractor(BASE_URL)
    all_products = await page_extractor.scrape_products_data(max_pages=30)
    c = ProductsController(all_products)

    print(f"\nProducts amount: {c.get_amount_of_products}\n")
    print(f"\nAverage price: {c.calculate_average_price}\n")
    print(f"\nProducts from the highest rates site:")
    pprint([product.to_dict for product in c.find_highest_rated_sites_products])
    print(f"\nThe lowest priced product from the highest rated site:")
    pprint(c.find_lowest_price_product_with_highest_rated_site.to_dict)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"\nExecution time: {execution_time} seconds")


if __name__ == "__main__":
    asyncio.run(main())