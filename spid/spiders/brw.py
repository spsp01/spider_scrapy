# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule




class MoreleSpider(CrawlSpider):
    name = 'brw'
    allowed_domains = ['brw.pl']
    start_urls = ['https://www.brw.pl']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        price = response.css('div[class=cena] *::text').extract_first().rstrip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t','').replace(',-','')
        if price !=[]:
            old_price=response.xpath('//span[@class="old-price stara-cena"]/text()').extract_first().replace(',-','')
            title = response.xpath('//title/text()').extract_first()
            h1 = response.xpath('//h1/text()').extract()[-1]
            category = response.xpath('//span[@itemprop="name"]/text()').extract()
            print(response.url)
            print(old_price,' ',price, ' ',title,' ',category)

    def categrystring(self):
        category =['BRW', 'meblościanki', 'nowoczesne']



