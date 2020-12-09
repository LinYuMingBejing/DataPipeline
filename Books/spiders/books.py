import scrapy
import re
from Books.items import BooksItem


keyDict = {'出版日期': 'published_date', 
            '語言': 'language', 
            '編者': 'author',
            '作者': 'author',
            '出版社': 'publisher',
            '譯者': 'translator',
            '原文作者': 'author',
            '原文出版社': 'publisher'}


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.books.com.tw']
    start_urls = ['https://www.books.com.tw/web/books_topm_01/?loc=P_0001_1_001']


    def parse(self, response):
        category_urls = response.xpath('//ul[@class="sub"]/li/span/a/@href').getall()
        
        if category_urls:
            for category_url in category_urls:
                yield scrapy.Request(category_url, callback=self.parse)    
        else:
            yield scrapy.Request(response.request.url, callback=self.parseInfoUrl, dont_filter=True)  


    def parseInfoUrl(self, response):
        info_urls = response.xpath('//div[@class="msg"]/h4/a/@href').getall()
        next_url = response.xpath('//a[@class="nxt"]/@href').get()
        
        for info_url in info_urls:
            yield scrapy.Request(info_url, callback=self.parseInfo)

        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)
    
    
    def parseInfo(self, response):
        item = BooksItem()
        item['page_url'] = response.request.url
        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('//strong[@class="price01"]//text()').get()
        item['mainCategory'] = response.xpath('//ul[@class="sort"]/li/a/text()').getall()[-2].strip()
        item['subCategory'] = response.xpath('//ul[@class="sort"]/li/a/text()').getall()[-1].strip()
        item['discount'] = response.xpath('//ul[@class="price"]/li/strong/b/text()').get()
        item['origin_price'] = response.xpath('//ul[@class="price"]/li/em/text()').get()
        
        descriptions = response.xpath('//div[@class="content"]//text()').getall()
        item['descriptions'] = ''.join(descriptions).strip()

        blocks = response.xpath('//div[@class="type02_p003 clearfix"]/ul/li')
        
        for block in blocks:
            if block.xpath('./span'):
                key = re.sub('：', '', block.xpath('./div/text()').get()).strip()
                value = block.xpath('./span//text()').get()

            elif block.xpath('./a'):
                key = re.sub('：', '', block.xpath('.//text()').get()).strip()
                value = block.xpath('./a//text()').get()

            else:
                text = block.xpath('./text()').get().split('：')
                key, value = text[0], text[1].strip()

            if key in keyDict:
                item[keyDict[key]] = value
    
        yield item