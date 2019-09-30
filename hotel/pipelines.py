# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

class HotelPipeline(object):
    def __init__(self):
        dbparams={
            'host' : '127.0.0.1',
            'port' : 3306,
            'user' : 'root',
            'password' : 'password',
            'database' : 'Hotel',
            'charset' : 'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        params = (item['title'],item['image'],item['address'],item['score'],item['count'],item['landlord_img'],item['house_info'],item['secnery_list'],item['secnery_list2'],item["comment_list"],item["go_time"],item["exit_time"],item["facility"],item['room_type'])
        self.cursor.execute(self.sql, params)
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql="""
            insert into booking(id, title, image, address, score, count, landlord_img, house_info, secnery_list, secnery_list2, comment_list, go_time, exit_time, facility, room_type)
            values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            return self._sql
        return self._sql
