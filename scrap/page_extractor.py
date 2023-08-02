import asyncio
import re
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from scrap.product import Product


class PageExtractor:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.products_from_all_pages = []

    @staticmethod
    async def _fetch_page(session: aiohttp.ClientSession, url: str) -> str:
        async with session.get(url, timeout=5) as response:
            return await response.text()

    @staticmethod
    def _extract_price(price_text: str) -> float:
        price_pattern = r'(\d[\d\s,]*\.\d{1,2}|\d[\d\s,]*)'
        match_price = re.search(price_pattern, price_text)
        return float(match_price.group(1).replace("&nbsp;", "").replace(",", "").replace("\xa0", ""))

    @staticmethod
    def _extract_rating(rating_text: str) -> float:
        rating_match = re.search(r'(\d+(\.\d+)?)', rating_text)
        return float(rating_match.group(1))

    async def _parse_products_from_single_page(self, session: aiohttp.ClientSession, offset: int) -> list[Product]:
        url = f"{self.base_url}&offset={offset}"
        response = await self._fetch_page(session, url)

        soup = BeautifulSoup(response, 'lxml')
        product_elements = soup.find_all('div', class_='item_box_main')

        products_from_single_page = []

        for product in product_elements:
            name = product.find('h2', class_='item_name').text

            price_span_text = product.find('div', class_='item_price').find('span').text
            price = self._extract_price(price_span_text)

            rating_element = product.find('img')['title']
            store_rating = self._extract_rating(rating_element)

            product_url = product.find("a", class_="item_link")["href"]
            website = urljoin(self.base_url, product_url)

            product = Product(
                name=name,
                price=price,
                store_rating=store_rating,
                website=website
            )

            products_from_single_page.append(product)

        return products_from_single_page

    async def scrape_products_data(self, max_pages: int) -> list[Product]:
        async with aiohttp.ClientSession() as session:
            offset = 0
            page_number = 0

            while page_number < max_pages:
                try:
                    products_from_single_page = await self._parse_products_from_single_page(session, offset)
                    if len(products_from_single_page) < 1:
                        print("\nResult:\n")
                        break
                    self.products_from_all_pages.extend(products_from_single_page)
                except asyncio.exceptions.TimeoutError or aiohttp.ClientTimeout:
                    print(f"Timeout occurred for URL: {self.base_url}")
                    await asyncio.sleep(2)
                    continue
                else:
                    page_number += 1
                    print(f"Fetching next page #{page_number}")
        return self.products_from_all_pages

