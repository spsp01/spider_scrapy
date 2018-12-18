# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MoreleSpider(CrawlSpider):
    name = 'morele'
    allowed_domains = ['morele.net']
    start_urls = ['https://www.morele.net/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        print(response.xpath('//*[@id="product_price_brutto"]/text()').extract())
