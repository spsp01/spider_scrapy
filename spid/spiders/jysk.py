# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spid.items import SpidItem


class JyskSpider(CrawlSpider):
    name = 'jysk'
    allowed_domains = ['jysk.pl']
    start_urls = ['https://jysk.pl/']

    rules = (
        Rule(LinkExtractor(deny=['\?page=','\?category=','email-friend']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = SpidItem()

        price = response.css('div[class=wishlist-button]::attr(data-price)').extract_first()

        item['category'] = 'inne'
        if price != None:
           item['category'] = 'produkt'
           item['price'] = price
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').extract_first()
        print(item)
        yield item



