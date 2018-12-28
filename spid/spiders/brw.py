# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spid.items import SpidItem


class MoreleSpider(CrawlSpider):
    name = 'brw'
    allowed_domains = ['brw.pl']
    start_urls = ['https://www.brw.pl/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = SpidItem()
        item['price']= response.css('div[class=cena] *::text').extract_first().rstrip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t','').replace(',-','')
        item['url'] = response.url
        print(item)
        yield item

