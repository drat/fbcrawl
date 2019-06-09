# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from scrapy.exceptions import DropItem
# from datetime import datetime
from sqlite3 import dbapi2 as sqlite

class FbcrawlPipeline(object):
    def __init__(self):
        self.connection = sqlite.connect('./post.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS post '
                            '(id INTEGER PRIMARY KEY, page VARCHAR(255),'
                            'post_id VARCHAR(255), date_crawl VARCHAR(255), data TEXT)')

#    def process_item(self, item, spider):
#        if item['date'] < datetime(2017,1,1).date():
#            raise DropItem("Dropping element because it's older than 01/01/2017")
#        elif item['date'] > datetime(2018,3,4).date():
#            raise DropItem("Dropping element because it's newer than 04/03/2018")
#        else:
#            return item
    def process_item(self, item, spider):
        self.cursor.execute("select * from post where xs_thu=? and xs_ngay_thang=? and xs_nam=?", (item['xs_info'][0], item['xs_info'][1], item['xs_info'][2]))

        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute(
                "insert into kq_xs (xs_thu, xs_ngay_thang, xs_nam, xs_data) values (?, ?, ?, ?)",
                (item['xs_info'][0], item['xs_info'][1], item['xs_info'][2], str(item['xs_data'])))

            self.connection.commit()

        return item
