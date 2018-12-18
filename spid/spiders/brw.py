# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MoreleSpider(CrawlSpider):
    name = 'brw'
    allowed_domains = ['brw.pl']
    start_urls = ['https://www.brw.pl/mebloscianka-fever-3,24928/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        price = response.css('div[class=cena] *::text').extract_first().rstrip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t','').replace(',-','')
        #if price !=[]:
        print(response.url)
        print(price)
