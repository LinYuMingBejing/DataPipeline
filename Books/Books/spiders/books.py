import scrapy
import re

keyDict = {'出版日期': 'published_date', 
            '語言': 'language', 
            '編者': 'author',
            '作者': 'author',
            '出版社': 'publisher',
            '原文出版社': 'publisher'}


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.books.com.tw']
    start_urls = ['https://www.books.com.tw/web/books_topm_01/?loc=P_0005_001']


    def parse(self, response):
        category_urls =  response.xpath('//ul[@class="sub"]/li/span/a/@href').getall()
        for category_url in category_urls:
            yield scrapy.Request(category_url, callback=self.parseInfoUrl)
    

    def parseInfoUrl(self, response):
        info_urls = response.xpath('//div[@class="msg"]/h4/a/@href').getall()
        next_url = response.xpath('//a[@class="nxt"]/@href').get()
        for info_url in info_urls:
            yield scrapy.Request(info_url, callback=self.parseInfo)
        
        yield scrapy.Request(next_url, callback=self.parse)
    
    
    def parseInfo(self, response):
        title  = response.xpath('//h1/text()').get()
        price = response.xpath('//strong[@class="price01"]//text()').get()
        category = response.xpath('//ul[@class="sort"]/li/a/text()').getall()[-1].strip()
        
        descriptions = response.xpath('//div[@class="content"]//text()').getall()
        descriptions = ''.join(descriptions).strip()
        
        blocks = response.xpath('//div[@class="type02_p003 clearfix"]/ul/li')
        bookInfo = []
        for block in blocks:
            row = {}
            key = re.sub('：', '', block.xpath('.//text()').get()).strip()

            if block.xpath('./span'):
                value = block.xpath('./span/text()').get()
            elif block.xpath('./a'):
                value = block.xpath('./a/text()').get()
            else:
                text = block.xpath('./text()').get().split('：')
                key, value = text[0], text[1].strip()

            if key in keyDict:
                row[keyDict[key]] = value

            bookInfo.append(row)

        
