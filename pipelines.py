# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import importlib
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import settings


class GubaPipeline(object):

    def __init__(self):
        dbargs = dict(
            host='localhost',
            db='jdjr_data',
            user='root',  # replace with you user name
            passwd='1111',  # replace with you password
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    def process_item(self, item):
        print 'ok'
        res = self.dbpool.runInteraction(self.insert_into_table, item)
        return item

    def insert_into_table(self, conn, item):
        #db_name = item.__class__.__name__
        conn.execute(
            'insert into tieba(cat_fir,cat_sec,title,attention_num,article_num,flag) values(%s,%s,%s,%s,%s,%s)', (
                item['cat_fir'], item['cat_sec'], item['title'], item['attention_num'], item['article_num'], item['flag']))

if __name__ == '__main__':
    pipline = GubaPipeline()
    pipline.process_item({'cat_fir':'111','cat_sec':'222','title':'333','attention_num':'44','article_num':'55','flag':'77'})
    print 'done'