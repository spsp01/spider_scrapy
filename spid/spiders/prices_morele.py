from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.item import Item, Field

class MyItem(Item):
    url= Field()


class someSpider(CrawlSpider):
    name = 'crawltest'
    allowed_domains = ['axa.pl']
    start_urls = ['https://axa.pl/']
    rules = (Rule(LxmlLinkExtractor(allow=()), callback='parse_obj', follow=True),)

    def parse_obj(self,response):
        item = MyItem()
        item['url'] = []
        print(response)
        for link in LxmlLinkExtractor(allow=(),deny = self.allowed_domains).extract_links(response):
            item['url'].append(link.url)
        return item