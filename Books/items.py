# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    origin_price = scrapy.Field()
    mainCategory = scrapy.Field()
    subCategory = scrapy.Field()
    descriptions = scrapy.Field()
    page_url = scrapy.Field()
    publisher = scrapy.Field()
    translator = scrapy.Field()
    language = scrapy.Field()
    published_date = scrapy.Field()
