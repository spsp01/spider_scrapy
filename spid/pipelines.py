# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class SpidPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.category_seen = set()
        self.product_seen = set()

    def process_item(self, item, spider):
        if 'id' and 'name' and 'parent_category_id' in item.keys():
            if item['id'] in self.category_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.category_seen.add(item['id'])
                return item

        if 'name' and 'category_id' and 'thumbnail_url' and 'url' in item.keys():
            print(item.keys())
            if item['url'] in self.product_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.product_seen.add(item['url'])
               # print(item['url'])
                return item
        return item
