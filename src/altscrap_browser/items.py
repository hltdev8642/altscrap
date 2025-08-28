import scrapy

class AlternativeItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    rating = scrapy.Field()
