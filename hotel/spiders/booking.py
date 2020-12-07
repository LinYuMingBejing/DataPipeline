# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from hotel.items import HotelItem
import re

class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['www.booking.com']
    base_domain = 'https://www.booking.com'
    cities = ['台北', '新北', '台中', '高雄', '北京', '上海', '東京', '河內', '曼谷', '吉隆坡']
    
    start_urls = [f'https://www.booking.com/{city}' for city in cities]
    

    def parse(self, response):
        info_urls = response.xpath('//a[@class=" sr_item_photo_link sr_hotel_preview_track  "]/@href').getall()
        next_urls = response.xpath('//nav/ul/li[3]/a/@href').get()
        for info_url in info_urls:
            yield scrapy.Request(self.base_domain + info_url, callback=self.parse_info)

        yield scrapy.Request(self.base_domain + next_urls, callback=self.parse)


    def parseTourist(self, response):
        tourists = []
        touristInfo = response.xpath("//li[@class='bui-list__item']")
        for t in touristInfo:
            row = {}
            row['tourist']  = t.xpath("./div/div/text()").getall()[0].strip()
            row['distance'] = t.xpath("./div/div/text()").getall()[1].strip()
            tourists.append(row)
        return tourists


    def parse_info(self, response):
        tourists = self.parseTourist(response)
        address = response.xpath("//p[@class='address address_clean']/span/text()").get().strip()

        title = response.xpath('//h2[@id="hp_hotel_name"]/text()').getall()[1].strip()
        image = response.xpath('//a[@target="_blank"]/@href').getall()
        comments = response.xpath("//span[@class='c-review__body']/text()").getall()
        
        facilities = response.xpath("//div[@class='hp_desc_important_facilities clearfix hp_desc_important_facilities--bui ']/div/text()").getall()
        facilities = [i.strip() for i in list(filter(lambda x: x != '\n', facilities))]

        description = response.xpath("//div[@id='property_description_content']/p/text()").getall()
        description = ''.join(description)
        
        stars = response.xpath("//div[@class='bui-review-score c-score']/div[@class='bui-review-score__badge']/text()").get()
        stars = stars[0] if stars else 0 
        
        ratings = response.xpath("//span[@class='hp__hotel_ratings']/span/i/@title").get()
        ratings = ratings[0] if ratings else 0

        bed_type = response.xpath("//div[@class='room-info']/a/text()").getall()
        bed_type = [i.strip() for i in list(filter(lambda x: x != '\n', bed_type))]         

        time = response.xpath('//span[@class="u-display-block"]/text()').getall()
        checkin_time  = re.sub('[\u4e00-\u9fa5]', '', time[0].strip())
        checkout_time  = re.sub('[\u4e00-\u9fa5]', '', time[1].strip())
        
        row = {
            'title': title, 'image': image, 'comments': comments, \
            'address': address, 'facilities': facilities, 'description': description, 'stars': stars,\
            'ratings': ratings, 'bed_type': bed_type, 'checkin_time': checkin_time, 'checkout_time': checkout_time
        }
        item = HotelItem(row)
        return item