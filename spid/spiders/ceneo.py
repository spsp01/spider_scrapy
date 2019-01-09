# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spid.items import CategoryItem, ProductPriceItem, ShopItem, ProductItem
#


class CeneoSpider(CrawlSpider):
    name = 'ceneo'
    allowed_domains = ['ceneo.pl']
    start_urls = ['https://www.ceneo.pl/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        # Category Item part
        # Example category page: https://www.ceneo.pl/Male_AGD_do_domu

        category = CategoryItem()
        id = response.xpath('///nav/dl/dd/span/@data-category-id').extract()
        if len(id) > 1 :
            category['id'] = id[-1]
            category['name'] = response.xpath('///nav/dl/dd/span/a/span/text()').extract()[-1]
            category['parent_category_id'] = response.xpath('///nav/dl/dd/span/@data-category-id').extract()[-2]
            yield category

        # Product Item part
        # Example product page: https://www.ceneo.pl/43598790

        if response.xpath('//div[contains(@class,"js_product-body")]'):
            product = ProductItem()
            product['name'] = response.xpath('//h1[contains(@class,"product-name")]/text()').extract_first().strip()
            product['category_id'] =response.xpath('///nav/dl/dd/span/@data-category-id').extract()[-1]
            product['thumbnail_url'] = response.xpath('//div[@id="product-carousel"]/div/a/img/@src').extract_first()
            product['url'] = response.url
            #print(product)
            yield product

        # Shop Item part
        # Example category page: https://www.ceneo.pl/sklepy/mediaexpert.pl-s10772

        if response.xpath('//article[@class="store-top"]'):
            shop = ShopItem()
            shop['name'] = response.xpath('//article/section/div[@class="main-info-container"]/'
                                          'div[@class="main-content-card"]/div[2]/div[2]/text()').extract_first().strip()
            shop['url'] = response.url
            shop['thumbnail_url'] = response.xpath('//div[@class="sb-data-shop-logo"]/img/@src').extract_first()
            #print(shop)
            yield shop

        # Product Price Item part
        # Example category page:  https://www.ceneo.pl/43598790

        if response.xpath('//table[contains(@class,"product-offers")]'):
            shop_id = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr[@data-trackinfotype="Click"]/@data-shop').extract()
            product_id = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr[@data-trackinfotype="Click"]/@data-productid').extract()
            price = self.price_sum(response)
            price_and_shipment = self.price_and_shipment(response)
            for idx, i in enumerate(shop_id):
                product_price = ProductPriceItem()
                product_price['shop_id']= shop_id[idx]
                product_price['product_id'] = product_id[idx]
                product_price['price'] = price[idx]
                product_price['price_and_shipment'] = price_and_shipment[idx]
               # print(product_price)
                yield product_price


    def price_sum(self,response):
        """
        Sums main value and penny value
        """
        value = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr/td[@class="cell-price"]/a/span/span/span[@class="value"]/text()').extract()
        penny = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr/td[@class="cell-price"]/a/span/span/span[@class="penny"]/text()').extract()

        penny_float = []
        for i in penny:
            penny_float.append(float(i.replace(',', '0.')))

        value_int = ([int(i) for i in value])
        prices =([x + y for x, y in zip(value_int, penny_float)])
        return prices

    def price_and_shipment(self,response):
        """
        Returns price and shipment value
        """
        rows = response.xpath('//table[contains(@class,"product-offers")]/tbody/tr/td[@class="cell-price"]//div[@class="product-delivery-info js_deliveryInfo"]').extract()
        price_ship = []

        for i in rows:
            #print(rows)
            if 'Z wysyłką' in i:
                price_ship.append(i.strip().replace('Z wysyłką od\r\n','').replace(' ','').replace('zł',''))
            if 'Darmowa wysyłka' in i:
                price_ship.append(0)
            if not 'Z wysyłką' and 'Darmowa wysyłka' in i:
                price_ship.append('N/A')
        print(price_ship)
        return price_ship