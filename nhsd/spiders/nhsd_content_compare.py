import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..items import NhsdItem
from ..items import ResourceItem
from twisted.python.failure import Failure

class NhsdContentSpider(scrapy.spiders.CrawlSpider):
    name = 'nhsd-content-compare'

    # Sites to compare
    reference_site = 'https://nhsd.io'
    test_site = 'https://uat2.nhsd.io'

    le = LinkExtractor(
        # Deny sub domains and search pages (infinite loops)
        deny=(['^.*\.nhsd\.io/', 'nhsd\.io/ndrs/search/.*', 'nhsd\.io/search/.*']),
        allow_domains=(['nhsd.io'])
    )

    start_url = reference_site

    allowed_domains = [
        urlparse(reference_site).hostname,
        urlparse(test_site).hostname,
    ]

    # Start crawling from the start_url
    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.crawl_pages)

    def crawl_pages(self, response):
        # for each page requested on the reference site, make a request to the test site
        # Include the response for the original request in the meta object
        altUrl = response.url.replace(self.reference_site, self.test_site)
        yield scrapy.Request(url=altUrl, meta={'origRes': response}, callback=self.parse, errback=self.parse)

        # Extract links from the page and process with crawl_pages method
        for link in self.le.extract_links(response):
            parsedUrl = urlparse(link.url)
            parsedUrlString = parsedUrl._replace(query='', fragment='').geturl()

            yield scrapy.Request(url=parsedUrlString, callback=self.crawl_pages)

    # Matches a resource (image, js, css, etc)
    # First confirms the test site didn't respond with an error
    # Then checks the response bodys match
    # The match result is then yielded back
    def match_resource(self, responseOrFailure):
        if isinstance(responseOrFailure, Failure):
            originalRes = responseOrFailure.request.meta['origRes']
            response = responseOrFailure.request
            match = False
        else:
            originalRes = responseOrFailure.meta['origRes']
            response = responseOrFailure
            match = False
            if (originalRes.body == response.body):
                match = True

        item = ResourceItem()
        item['url'] = originalRes.url
        item['alt_url'] = response.url
        item['match'] = match

        yield item

    # Request the resource and send response to the matcher method
    def check_resource(self, response):
        altResource = response.url.replace(self.reference_site, self.test_site)
        yield scrapy.Request(url=altResource, meta={'origRes': response}, callback=self.match_resource, errback=self.match_resource)

    # Process page response
    def parse(self, responseOrFailure):
        # Check if reference and test pages match...
        # First check test site didn't error, then send request responses to match_res method to match content
        match = False
        if isinstance(responseOrFailure, Failure):
            originalRes = responseOrFailure.request.meta['origRes']
            response = responseOrFailure.request
        else:
            originalRes = responseOrFailure.meta['origRes']
            response = responseOrFailure
            if 'text' in dir(originalRes):
                match = self.match_res(originalRes, response)

        # If the response isn't empty, yield back the match result for this page
        if 'text' in dir(originalRes):
            item = NhsdItem()
            item['page_title'] = originalRes.xpath('//title/text()').get()
            item['url'] = originalRes.url
            item['alt_url'] = response.url
            item['match'] = match

            yield item

        # Pull <script>, <img> & <link> resources
        scripts = originalRes.xpath("//script/@src").extract()
        imgs = originalRes.xpath("//img/@src").extract()
        links = originalRes.xpath("//link/@href").extract()

        resources = scripts + imgs + links

        # Request reference resources and process with check_resource method
        for resource in resources:
            if len(resource) <= 500:
                resourceLink = originalRes.urljoin(resource)
                yield scrapy.Request(url=resourceLink, callback=self.check_resource)

    # Matches site pages by comparing page text and http status codes
    def match_res(self, res1, res2):
        res1Text = ", ".join(res1.xpath("//body//*[not(name()='script')]//text()").extract())
        res2Text = ", ".join(res2.xpath("//body//*[not(name()='script')]//text()").extract())

        if res1Text != res2Text:
            return False

        if res1.status != res2.status:
            return False

        return True
