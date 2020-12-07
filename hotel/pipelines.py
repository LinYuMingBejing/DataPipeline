# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient


class HotelPipeline(object):

    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'booking')
        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client[db_name]


    def process_item(self, item, spider):
        self.insert_article(item)
        return item


    def insert_article(self, item):
        item = dict(item)
        self.db.article.update({'title': item['title']}, {'$set': item}, upsert=True)


    def close_spider(self, spider):
        self.db_clients.close()
