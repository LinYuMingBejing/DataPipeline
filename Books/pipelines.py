# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BooksPipeline:
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI')
        db_name = spider.settings.get('MONGODB_DB_NAME')
        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client[db_name]


    def process_item(self, item, spider):
        self.insert_article(item)
        return item
    

    def process_type(self, item):
        if 'price' in item:
            item['price'] = int(item['price'])
        if 'discount' in item:
            item['discount'] = float(item['discount'])
        if 'origin_price' in item:
            item['origin_price'] = int(item['origin_price'])
        if 'published_date' in item:
            item['published_date'] = datetime.strptime(item['published_date'], '%Y/%m/%d')
        return item


    def insert_article(self, item):
        item = self.process_type(dict(item))
        self.db.article.update({'title': item['title']}, {'$set': item}, upsert=True)


    def close_spider(self, spider):
        self.db_clients.close()
