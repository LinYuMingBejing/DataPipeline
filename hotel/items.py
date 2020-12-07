# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    comments = scrapy.Field()
    address = scrapy.Field()
    facilities = scrapy.Field()
    description = scrapy.Field()
    stars = scrapy.Field()
    ratings = scrapy.Field()
    bed_type = scrapy.Field()
    checkin_time = scrapy.Field() 
    checkout_time = scrapy.Field()