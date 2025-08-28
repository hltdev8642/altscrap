import scrapy
from altscrap_browser.items import AlternativeItem

class AlternativetoSpider(scrapy.Spider):
    name = 'alternativeto'
    allowed_domains = ['alternativeto.net']

    def __init__(self, software_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if software_name:
            self.start_urls = [f'https://alternativeto.net/software/{software_name}']
        else:
            self.start_urls = []

    def parse(self, response):
        # Extract alternatives
        alternatives = response.css('div.app')  # Assuming each alternative is in a div with class 'app'
        for alt in alternatives:
            item = AlternativeItem()
            item['name'] = alt.css('h2 a::text').get()
            item['description'] = alt.css('p.description::text').get()
            item['url'] = alt.css('h2 a::attr(href)').get()
            item['rating'] = alt.css('.rating::text').get()
            yield item
