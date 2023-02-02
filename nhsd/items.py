# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NhsdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page_title = scrapy.Field()
    url = scrapy.Field()
    alt_url = scrapy.Field()
    match = scrapy.Field()

class ResourceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    alt_url = scrapy.Field()
    match = scrapy.Field()

class SitemapItem(scrapy.Item):
    url = scrapy.Field()
    redirects = scrapy.Field()
