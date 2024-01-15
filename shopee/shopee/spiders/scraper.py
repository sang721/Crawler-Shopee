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
        yield Request(url=url, headers=self.headers, callback=self.test_1)

    def test_1(self, response):
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
            for each_page in range(number_of_page):
                offset = 0 if number_of_page <= 1 else (number_of_page * limit_per_page) - number_of_page
                # Get all products
                url = (f"https://mall.shopee.vn/api/v4/recommend/recommend?bundle=mall_popular&catId={cat_id}&"
                       f"item_card=2&limit={limit_per_page}&offset={offset}")
                r = requests.get(url=url, headers=self.headers)
                data = r.json()
                yield data



