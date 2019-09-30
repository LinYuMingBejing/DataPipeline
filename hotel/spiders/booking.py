# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from hotel.items import HotelItem
class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['www.booking.com']
    base_domain = "https://www.booking.com"
    urls = 'https://www.booking.com/{}'
    cities = ["台北","新北","台中","高雄","北京","上海","東京","河內","曼谷","吉隆坡"]
    start_urls = []
    # 爬取亞洲各大城市的飯店
    for city in cities:
        start_urls.append(urls.format(city))
    
    

    def parse(self, response):
        # 分析詳情頁面url 以及 下一頁的url
        info_urls = response.xpath('//a[@class=" sr_item_photo_link sr_hotel_preview_track  "]/@href').getall()
        next_urls = response.xpath('//nav/ul/li[3]/a/@href').get()
        for info_url in info_urls:
            yield scrapy.Request(self.base_domain+info_url, callback=self.parse_info)

        yield scrapy.Request(self.base_domain+next_urls, callback=self.parse)

    def parse_info(self, response):
        # 飯店資訊
        title = response.xpath('//h2[@class="hp__hotel-name"]/text()').getall()[1].replace("\n","")
        image = response.xpath('//div[@id="photos_distinct"]/a/@href').getall()
        image = ",".join(image)
        address = response.xpath("//p[@class='address address_clean']/span/text()").get().strip()
        
        score = response.xpath("//div[@class='bui-review-score__badge']/text()").get()
        if score:
            score = float(score.split(" ")[1])
        else:
            score = float(score)
        
        count = response.xpath('//div[@class="bui-review-score__text"]/text()').get().split(" ")[1]
        if "," in count:
            count = count.split(",")
            count = int("".join(count))
        count = int(count)

        landlord_img = response.xpath('//img[@class="bui-avatar__image hops__host-photo js-host-info__photo js-host-info__photo--photo"]/@src').get()
        
        house_info = response.xpath('//div[@id="property_description_content"]/p//text()').getall()
        house_info = ",".join(house_info)
        # 附近人文景點
        secnery = response.xpath('//ul[@class="bui-list bui-list--text hp-poi-list__wrapper"]/li/div/div/text()').getall()
        distance = response.xpath('//ul[@class="bui-list bui-list--text hp-poi-list__wrapper"]/li/div/span/text()').getall()
        secnery_list = list()

        for tourism in zip(secnery,distance):
            secnery=tourism[0].replace("\n","")
            distance=tourism[1].replace("\n","")
            tourism=secnery,distance
            secnery_list.append(tourism)
        
        secnery_list = str(secnery_list).split("[")[1].split("]")[0].replace("(","").replace(")","|").replace("'","").replace(",","")
        
        # 附近自然景點
        secnery_list2 = list()
        landscape = response.xpath('//ul[@class="bui-list bui-list--text add hp-poi-list__wrapper"]/li/div/div/span[1]/text()').getall()
        distance = response.xpath('//ul[@class="bui-list bui-list--text add hp-poi-list__wrapper"]/li/div/span/text()').getall()
        for tourism in zip(landscape,distance):
            secnery=tourism[0].replace("\n","")
            distance=tourism[1].replace("\n","")
            tourism=secnery,distance
            secnery_list2.append(tourism)
        
        secnery_list2 = str(secnery_list2).split("[")[1].split("]")[0].replace("(","").replace(")","|").replace("'","").replace(",","")

        # 爬取評論
        comment_list = []
        selectors = response.xpath('//div[@class="reviews-snippet-sidebar__item"]')
        for selector in selectors:
            img = selector.xpath('.//img/@src').get()
            author = selector.xpath('.//span[@class="bui-avatar-block__title"]/text()').get()
            comment = selector.xpath('.//span[@class="c-review__body"]/text()').get()
            comment_info = img,author,comment
            comment_list.append(comment_info)
        comment_list = str(comment_list).split("[")[1].split("]")[0].replace("(","").replace(")","|").replace("'","").replace(",","")

        # 入住、退宿時間
        time = response.xpath('//span[@class="u-display-block"]/text()').getall()
        go_time = time[0].replace("\n","")
        exit_time = time[1].replace("\n","")
        
        #  飯店設施
        facility = response.xpath('//div[1][@class="hp_desc_important_facilities clearfix "]/div/text()').getall()[1::2]
        facility_list=[]
        for f in facility:
            facility_list.append(f.replace("\n",""))
        facility_list = str(facility_list).split("[")[1].split("]")[0].replace("(","").replace(")","|").replace("'","").replace(",","")
        
        # 房型
        selectors = response.xpath('//div[@class="room-info"]')
        room_list = list()
        for selector in selectors:
            try:
                room_type = selector.xpath('.//a[@class="jqrt togglelink"]/text()').getall()[-1].replace("\n","")
                room_type1 = selector.xpath('.//li[@class="rt-bed-type"]/span/text()').getall()[0].replace("\n","")
                room = room_type,room_type1
                room_list.append(room)
            except:
                continue
        room_type = str(room_list).split("[")[1].split("]")[0].replace("(","").replace(")","|").replace("'","").replace(",","")

        item = HotelItem(title=title,address=address,score=score,count=count,landlord_img=landlord_img,house_info=house_info,image=image,secnery_list=secnery_list, \
        secnery_list2=secnery_list2,comment_list=comment_list,go_time=go_time,exit_time=exit_time,facility=facility_list,room_type=room_type)
        return item