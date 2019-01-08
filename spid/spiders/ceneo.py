# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spid.items import CategoryItem


class CeneoSpider(CrawlSpider):
    name = 'ceneo'
    allowed_domains = ['ceneo.pl']
    start_urls = ['https://ceneo.pl/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        category = CategoryItem()
        category['id'] = response.xpath('//nav/dl/dd/span/@data-category-id').extract()[-1]
        category['name'] = response.xpath('//nav/dl/dd/span/a/span/text()').extract()[-1]
        category['parent category id']=response.xpath('//nav/dl/dd/span/@data-category-id').extract()[-2]
        print(category)
        return category



