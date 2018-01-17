# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from TTSpider import settings
# import time
import logging
import sys


logger = logging.getLogger()

class TTSpiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8')
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        sql = '''INSERT INTO TTUser (name, url) VALUES ("%s", "%s");''' % \
        (   
            self.connect.escape(item['name']), 
            item['url']
        )
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except pymysql.err.IntegrityError:
            pass
        except Exception as err:
            # print(sql)
            # self.connect.rollback()
            logging.log(logging.ERROR, err)
            try:
                sql = '''INSERT INTO TTUser (name, url) VALUES ("%s", "%s");''' % \
                    (   
                        '', 
                        item['url']
                    )
                self.cursor.execute(sql)
                self.connect.commit()
            except Exception as e:
                pass
        else:
            logger.info('Insert successful')
            return item