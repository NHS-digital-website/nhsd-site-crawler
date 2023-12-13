import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..items import SitemapItem

# Simple spider script to crawl site and yield back urls, along with redirections

class NhsdSitemapSpider(scrapy.spiders.CrawlSpider):
    name = 'nhsd-sitemap-generator'

    start_url = 'https://digital.nhs.uk/'
    base_url = 'https://digital.nhs.uk'

    allowed_domains = ['digital.nhs.uk']
    response_type_whitelist = ['text/html']

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.crawl_pages)

    def crawl_pages(self, response):
        yield self.parse(response)

        for link in LinkExtractor(
            deny=([
                '/binaries/.*',
                '/search/.*',
                '/cyber-alerts/.*(?:.*(?:threat_type|year|severity|month).+)',
                '/developer/.*(?:filter=).*',
                '/services/service-catalogue/.*(?:filter=).*',
                r'/news/feed/year/\d{4}.*',
                '/news-and-events/.*(?:year|month).*',
                '/news/events/.*(?:type=).*',
                '/ndrs/.*',
                '/error/.*'
            ]),
            allow_domains=([
                'digital.nhs.uk',
                'files.digital.nhs.uk'
            ])
        ).extract_links(response):
            parsedUrl = urlparse(link.url)
            parsedUrlString = parsedUrl._replace(query='', fragment='').geturl()

            yield scrapy.Request(url=parsedUrlString, callback=self.crawl_pages)

    def parse(self, response):
        print(response.request.meta)
        item = SitemapItem()
        item['url'] = response.url
        if 'redirect_urls' in response.request.meta:
            item['redirects'] = response.request.meta['redirect_urls']
        else:
            item['redirects'] = []

        return item