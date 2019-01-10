# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter


class SpidPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesExportPipeline(object):

    def __init__(self):
        self.category_seen = set()
        self.product_seen = set()
        self.shop_seen = set()
        self.product_price_seen = set()

    def open_spider(self, spider):
        # Creates 4 files for storage scraped items
        self.category_file = open('spid/scraped/category.json', 'wb')
        self.category_exporter = JsonItemExporter(self.category_file, encoding="utf-8")
        self.category_exporter.start_exporting()
        self.product_file = open('spid/scraped/product.json', 'wb')
        self.product_exporter = JsonItemExporter(self.product_file, encoding="utf-8")
        self.product_exporter.start_exporting()
        self.shop_file = open('spid/scraped/shop.json', 'wb')
        self.shop_exporter = JsonItemExporter(self.shop_file, encoding="utf-8")
        self.shop_exporter.start_exporting()
        self.product_price_file = open('spid/scraped/productprice.json', 'wb')
        self.product_price_exporter = JsonItemExporter(self.product_price_file, encoding="utf-8")
        self.product_price_exporter.start_exporting()

    def close_spider(self, spider):
        # Closing exports and scraped item files

        self.category_exporter.finish_exporting()
        self.category_file.close()
        self.product_exporter.finish_exporting()
        self.product_file.close()
        self.shop_exporter.finish_exporting()
        self.shop_file.close()
        self.product_price_exporter.finish_exporting()
        self.product_price_file.close()

    def process_item(self, item, spider):
        if 'id' in item.keys() and 'name' in item.keys() and 'parent_category_id' in item.keys():

            if item['id'] in self.category_seen:
                raise DropItem("Duplicate category item found: %s" % item)
            else:
                self.category_seen.add(item['id'])
                self.category_exporter.export_item(item)
                return item

        if 'name' in item.keys() and 'category_id' in item.keys() and 'thumbnail_url' in item.keys() and 'url' in item.keys():

            if item['url'] in self.product_seen:
                raise DropItem("Duplicate product item found: %s" % item)
            else:
                self.product_seen.add(item['url'])
                self.product_exporter.export_item(item)
                return item

        if 'name' in item.keys() and 'url' in item.keys() and 'thumbnail_url' in item.keys():

            if item['url'] in self.shop_seen:
                print('Duplicate-Shop-found')
                raise DropItem("Duplicate shop item found: %s" % item)

            else:

                self.shop_seen.add(item['url'])
                self.shop_exporter.export_item(item)
                return item

        if 'shop_id' in item.keys() and 'product_id' in item.keys() and 'price' in item.keys() and 'price_and_shipment' in item.keys():

            if item['shop_id'] + '-' + item['product_id'] in self.product_price_seen:
                raise DropItem("Duplicate product price item found: %s" % item)
            else:
                self.product_price_seen.add(item['shop_id'] + '-' + item['product_id'])
                self.product_price_exporter.export_item(item)
                return item

        return item
