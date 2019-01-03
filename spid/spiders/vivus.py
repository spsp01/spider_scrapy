# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import html2text

class VivusSpider(CrawlSpider):
    name = 'vivus'
    allowed_domains = ['vivus.pl']
    start_urls = ['http://vivus.pl/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        i['url'] = response.url
        i['h1'] = response.xpath('//h1/text()').extract_first()
        i['article_len'] = self.lenarticle(response)
        i['num_h2'] = self.number_of_hx(response,'h2')
        i['num_h3'] = self.number_of_hx(response,'h3')
        i['num_images_article'] = self.extractimg(response)
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        i['num_links_article']= self.numberofinternallinks(response)
        print(i)
        return i

    def rawtext(self,html):
        #Returns raw text from html
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.bypass_tables = False
        text = text_maker.handle(html)
        return text

    def lenarticle(self,response):
        article = response.xpath('//*[@id="main"]/div/div/div[1]/article/div/div[1]').extract_first()

        if article != None:
           articlelen= len(self.rawtext(article))
        else:
            articlelen= 0
        return articlelen
    def number_of_hx(self,response,h):
        #Number of Hx header (H1,H2, etc.)
        hx = response.xpath('//'+h).extract()
        return len(hx)

    def extractimg(self, response):
        images_width = response.xpath('//*[@id="main"]/div/div/div[1]/article//img/@height').extract()
        images_width_int =  [int(i) for i in images_width]
        images_width_50 = [x for x in images_width_int if x > 50]
        return len(images_width_50)

    def numberofinternallinks(self,response):
        links_article =response.xpath('//*[@id="main"]/div/div/div[1]/article//a/@href').extract()
        internal_links_article =[]
        for i in links_article:
           if 'vivus.pl' in i:
               internal_links_article.append(i)
        return len(internal_links_article)
