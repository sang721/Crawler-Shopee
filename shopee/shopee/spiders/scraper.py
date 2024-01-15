import requests
import scrapy

from scrapy.crawler import CrawlerProcess
from scrapy import Request
from scrapy.utils.project import get_project_settings


class Scraper(scrapy.Spider):
    name = "shopee"

    def start_requests(self):
        """
        TEST 1
        Get all categories
        Returns:

        """
        url = 'https://mall.shopee.vn/api/v4/official_shop/get_categories_and_mall_shops'
        yield Request(url=url, headers=self.headers, callback=self.parse_parent_category)

    def parse_parent_category(self, response):
        """
        Get small categories
        Args:
            response:

        Returns:

        """
        data = response.json()
        # All shopee categories
        categories = data['data']['categories']
        for each_category in categories:
            cat_id = each_category['category_id']
            url = f'https://mall.shopee.vn/api/v4/official_shop/get_categories_and_mall_shops?parent_catid={cat_id}'
            yield Request(url=url, headers=self.headers, callback=self.parse_small_category,
                          meta={"category_id": cat_id})

    def parse_small_category(self, response):
        """
        TEST 2
        Get products in every category
        Args:
            max_product_per_page: can be set inside config.json
            number_of_page_per_category: can be set inside config.json

        Returns:
            Data >> Pipelines
        """
        data = response.json()
        limit_per_page = self.config.get('max_product_per_page')
        number_of_page = self.config.get('number_of_page_per_category')
        # All shopee categories
        categories = data['data']['categories']
        for each_category in categories:
            cat_id = each_category['category_id']
            for page_number in range(1, number_of_page + 1):
                offset = (page_number - 1) * limit_per_page
                # Get all products
                url = (f"https://mall.shopee.vn/api/v4/recommend/recommend?bundle=mall_popular&catId="
                       f"{cat_id}&item_card=2&limit={limit_per_page}&offset={offset}")

                r = requests.get(url=url, headers=self.headers)
                data = r.json()

                yield data
