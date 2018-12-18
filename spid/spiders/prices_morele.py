# -*- coding: utf-8 -*-
import scrapy


# class PricesMoreleSpider(scrapy.Spider):
#     name = 'prices_morele'
#     start_urls = ['https://www.morele.net/']
#
#     def parse(self, response):
#         self.valid_url.append({'url': response.url,
#                                'from': from_url,
#                                'text': from_text})
#
#         print(response)

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))