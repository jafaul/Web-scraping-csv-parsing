import asyncio
import re
import time
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup


async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, timeout=1) as response:
        return await response.text()


async def parse_product_page(session: aiohttp.ClientSession, base_url: str, offset: int) -> list[dict[str, float]]:
    products = []

    url = f"{base_url}&offset={offset}"
    response = await fetch_page(session, url)

    soup = BeautifulSoup(response, 'lxml')
    product_elements = soup.find_all('div', class_='item_box_main')

    for product in product_elements:
        name = product.find('h2', class_='item_name').text

        price_span_text = product.find('div', class_='item_price').find('span').text
        price_pattern = r'(\d[\d\s,]*\.\d{1,2}|\d[\d\s,]*)'

        match_price = re.search(price_pattern, price_span_text)
        price = float(match_price.group(1).replace("&nbsp;", "").replace(",", "").replace("\xa0", ""))

        rating_element = product.find('img')['title']
        rating_match = re.search(r'(\d+(\.\d+)?)', rating_element)
        store_rating = float(rating_match.group(1))

        product_url = product.find("a", class_="item_link")["href"]
        store_url = urljoin(base_url, product_url)

        products.append({"name": name, "price": price, "store_rating": store_rating, "website": store_url})

    return products


async def scrape_product_data(url: str) -> list[dict[str, float]]:
    products = []
    async with aiohttp.ClientSession() as session:
        offset = 0
        page_number = 1
        max_pages = 50
        while page_number <= max_pages:
            try:
                product_page = await parse_product_page(session, url, offset)
                if len(product_page) < 1:
                    print("\nResult:\n")
                    break
                products.extend(product_page)
                offset += 18

            except aiohttp.ClientTimeout:
                print(f"Timeout occurred for URL: {url}")
                await asyncio.sleep(2)
                continue
            else:
                page_number += 1
                print(f"Fetching next page #{page_number}")

    return products


def calculate_average_price(products: list) -> float:
    total_price = sum(product['price'] for product in products)
    return total_price / len(products)


def find_highest_rated_site(products):
    return max(products, key=lambda x: x['store_rating'] if x['store_rating'] is not None else float('-inf'))


def find_lowest_price_product_with_highest_rated_site(products) -> dict:
    highest_rating = find_highest_rated_site(products)["store_rating"]
    lowest_price_product = None
    for product in products:
        if product["store_rating"] == highest_rating:
            if lowest_price_product is None or product["price"] < lowest_price_product["price"]:
                lowest_price_product = product
    return lowest_price_product


if __name__ == "__main__":
    website_url = "https://www.salidzini.lv/cena?q=iphone+14+pro+128gb&acc=1"
    start_time = time.perf_counter()
    # scraped_data = scrape_product_data(website_url)
    scraped_data = asyncio.run(scrape_product_data(website_url))
    print(f"Products amount: {len(scraped_data)}")
    print(f"Average price: {calculate_average_price(scraped_data)}")
    print(
        f"""The lowest priced product from the highest rated site:{(
            find_lowest_price_product_with_highest_rated_site(scraped_data)
        )}"""
    )
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

