import json
import re
import pandas


class ScraperPipeLine:

    def convert_to_sku(self, input_string, shop_id, prod_id):
        cleaned_name = ''.join(e if e.isalnum() or e.isspace() else ' ' for e in input_string)
        cleaned_name = cleaned_name.replace(" ", "-")
        cleaned_name = re.sub('-+', '-', cleaned_name)

        return cleaned_name + f"-i.{prod_id}.{shop_id}"

    def open_spider(self, spider):
        """OPEN SPIDER FOR CONFIGURATION"""
        with open("config.json", "r") as json_file:
            spider.config = json.load(json_file)
        spider.headers = {
            "Host": "mall.shopee.vn",
            "Connection": "keep-alive",
            "x-shopee-language": "vi",
            "User-Agent": "iOS app iPhone Shopee appver=31626 language=vi app_type=1 Cronet/102.0.5005.61",
            "af-ac-enc-dat": spider.config.get("af-ac-enc-dat"),
            "X-Shopee-Client-Timezone": "Asia/Ho_Chi_Minh",
            "Cookie": spider.config.get("Cookie"),
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "vi-VN,vi,fr-FR,fr,en-US,en",
        }
        spider.total_data = []

    def process_item(self, item, spider):
        """ITEM PROCESS HERE"""
        items = item['data']['sections'][0]['data']['item']
        for each_item in items:
            shop_id = each_item['itemid']
            product_id = each_item['shopid']
            product = {}
            product['product_name'] = each_item['name']
            product['product_url'] = "https://shopee.vn/" + self.convert_to_sku(input_string=each_item['name'],
                                                                                shop_id=shop_id,
                                                                                prod_id=product_id)
            product['product_rating'] = each_item['item_rating']['rating_star']
            product['product_price'] = each_item['price']
            product['product_revenue'] = int(each_item['price']) * int(each_item['historical_sold'])
            spider.total_data.append(product)

    def close_spider(self, spider):
        """CLOSE CRAWLER WHEN ITEM IS DONE"""
        df = pandas.DataFrame(spider.total_data)
        df.to_excel(spider.config.get("data_folder"), engine="xlsxwriter", index=False)
