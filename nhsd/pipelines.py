# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from .items import NhsdItem
from .items import ResourceItem
from .items import ResourceItem
from .items import SitemapItem

class NhsdPipeline:
    def process_item(self, item, spider):
        return item

class CsvExportPipeline(object):
    def __init__(self):
        if not os.path.exists('results'):
            os.makedirs('results')
        file = open('results/pages.csv', 'wb')
        self.exporter = CsvItemExporter(file, str)
        self.exporter.fields_to_export = ['page_title', 'match', 'url', 'alt_url']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, NhsdItem):
            self.exporter.export_item(item)

        return item

class CsvResourceExportPipeline(object):
    def __init__(self):
        file = open('results/resources.csv', 'wb')
        self.exporter = CsvItemExporter(file, str)
        self.exporter.fields_to_export = ['match', 'url', 'alt_url']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, ResourceItem):
            self.exporter.export_item(item)

        return item

class CsvSitemapExportPipeline(object):
    def __init__(self):
        file = open('results/sitemap.csv', 'wb')
        self.sitemapExporter = CsvItemExporter(file, str)
        self.sitemapExporter.fields_to_export = ['url', 'redirects']
        self.sitemapExporter.start_exporting()

    def spider_closed(self, spider):
        self.sitemapExporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, SitemapItem):
            self.sitemapExporter.export_item(item)

        return item
