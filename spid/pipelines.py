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
        self.shop_seen = set()

    def process_item(self, item, spider):

        # Removes duplicates from Category Item
        if 'id' in item.keys() and 'name' in item.keys() and 'parent_category_id' in item.keys():
            if item['id'] in self.category_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.category_seen.add(item['id'])
                return item

        # Removes duplicates from Product Item
        if 'name' in item.keys() and 'category_id' in item.keys() and 'thumbnail_url' in item.keys() and 'url' in item.keys():

            if item['url'] in self.product_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.product_seen.add(item['url'])
                return item

        # Removes duplicates from Shop Item
        if 'name' in item.keys() and 'url' in item.keys() and 'thumbnail_url' in item.keys():

            if item['url'] in self.shop_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.shop_seen.add(item['url'])
                return item

        # Removes duplicates from Shop Item
        if 'name' in item.keys() and 'url' in item.keys() and 'thumbnail_url' in item.keys():

            if item['url'] in self.shop_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.shop_seen.add(item['url'])
                return item
        return item
