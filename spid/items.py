# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidItem(scrapy.Item):
    price = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()


class CategoryItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    parent_category_id = scrapy.Field()


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    category_id = scrapy.Field()
    thumbnail_url = scrapy.Field()
    url = scrapy.Field()


class ShopItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    thumbnail_url = scrapy.Field()


class ProductPriceItem(scrapy.Item):
    shop_id = scrapy.Field()
    product_id = scrapy.Field()
    price = scrapy.Field()
    price_and_shipment = scrapy.Field()
