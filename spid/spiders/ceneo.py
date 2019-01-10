# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spid.items import CategoryItem, ProductPriceItem, ShopItem, ProductItem
from bs4 import BeautifulSoup


class CeneoSpider(CrawlSpider):
    name = 'ceneo'
    allowed_domains = ['ceneo.pl']
    start_urls = ['https://www.ceneo.pl/']

    rules = (
        Rule(LinkExtractor(deny=('\;','opinie-')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        # Category Item part
        # Example category page: https://www.ceneo.pl/Male_AGD_do_domu

        category = CategoryItem()
        id = response.xpath('///nav/dl/dd/span/@data-category-id').extract()
        if len(id) > 1:
            category['id'] = id[-1]
            category['name'] = response.xpath('///nav/dl/dd/span/a/span/text()').extract()[-1]
            category['parent_category_id'] = response.xpath('///nav/dl/dd/span/@data-category-id').extract()[-2]
            yield category

        # Product Item part
        # Example product page: https://www.ceneo.pl/43598790

        if response.xpath('//div[contains(@class,"js_product-body")]'):
            product = ProductItem()
            product['name'] = response.xpath('//h1[contains(@class,"product-name")]/text()').extract_first().strip()
            product['category_id'] = response.xpath('///nav/dl/dd/span/@data-category-id').extract()[-1]
            product['thumbnail_url'] = response.xpath('//div[@id="product-carousel"]/div/a/img/@src').extract_first()
            product['url'] = response.url
            product['score'] = response.xpath('//span[@class="product-score"]/@content').extract_first()
            product['review_count'] = response.xpath('//span[@itemprop="reviewCount"]/text()').extract_first()
            print(product)
            yield product

        # Shop Item part
        # Example category page: https://www.ceneo.pl/sklepy/mediaexpert.pl-s10772

        if response.xpath('//article[@class="store-top"]'):
            shop = ShopItem()
            shop['name'] = response.xpath('//article/section/div[@class="main-info-container"]/'
                                          'div[@class="main-content-card"]/div[2]/div[2]/text()').extract_first().strip()
            shop['url'] = response.url
            shop['thumbnail_url'] = response.xpath('//div[@class="sb-data-shop-logo"]/img/@src').extract_first()

            yield shop

        # Product Price Item part
        # Example category page:  https://www.ceneo.pl/43598790

        if response.xpath('//table[contains(@class,"product-offers")]'):
            shop_id = response.xpath('//table[contains(@class,"product-offers")]/tbody'
                                     '/tr[@data-trackinfotype="Click"]/@data-shop').extract()
            product_id = response.xpath('//table[contains(@class,"product-offers")]/tbody'
                                        '/tr[@data-trackinfotype="Click"]/@data-productid').extract()
            price = self.price_sum(response)
            price_and_shipment = self.price_and_shipment(response, price)
            product_url = response.xpath('//td[@class="cell-actions"]/a[contains(@class,"go-to-shop")]/@href').extract()


            for idx, i in enumerate(shop_id):
                product_price = ProductPriceItem()
                product_price['shop_id'] = shop_id[idx]
                product_price['product_id'] = product_id[idx]
                product_price['price'] = price[idx]
                product_price['price_and_shipment'] = price_and_shipment[idx]
                product_price['product_url'] =  'https://www.ceneo.pl/'+product_url[idx]

                yield product_price

    def price_sum(self, response):
        """
        Sums main value and penny value
        """
        value = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr/td[@class="cell-price"]'
                               '/a/span/span/span[@class="value"]/text()').extract()
        penny = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr/td[@class="cell-price"]'
                               '/a/span/span/span[@class="penny"]/text()').extract()

        penny_float = []

        for i in penny:
            penny_float.append(float(i.replace(',', '0.')))

        value_int = ([int(i) for i in value])
        prices = ([x + y for x, y in zip(value_int, penny_float)])

        return prices

    def price_and_shipment(self, response, price):
        """
        Returns price and shipment value
        """
        rows = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr/td[@class="cell-price"]'
                              '/div[@class="align-right"]/div').extract()
        price_ship = []

        for idx, i in enumerate(rows):
            if 'Z wysyłką' in i:
                soup = BeautifulSoup(i, 'lxml')
                pricefloat = float(
                    soup.get_text().strip().replace('Z wysyłką od\r\n', '').replace(' ', '').replace('zł', '')
                        .replace(',', '.'))
                price_ship.append(pricefloat)

            else:
                price_ship.append(price[idx])

        return price_ship
