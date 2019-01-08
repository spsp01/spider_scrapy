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
    patent_category_id = scrapy.Field()


