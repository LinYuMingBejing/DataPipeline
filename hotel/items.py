# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    address = scrapy.Field()
    score = scrapy.Field()
    count = scrapy.Field()
    landlord_img = scrapy.Field()
    house_info = scrapy.Field()
    secnery_list = scrapy.Field()
    secnery_list2 = scrapy.Field()
    comment_list = scrapy.Field()
    go_time = scrapy.Field()
    exit_time = scrapy.Field()
    facility = scrapy.Field()
    room_type = scrapy.Field()
