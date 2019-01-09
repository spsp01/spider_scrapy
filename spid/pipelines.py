# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
class SpidPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):

        if 'thumbnail_url' in item:
            print(item)
        return item
