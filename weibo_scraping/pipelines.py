# -*- coding: utf-8 -*-

import sqlite3

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeiboConsolePipeline(object):
    def process_item(self, item, spider):
        return item


class WeiboSqlitePipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect('weibo.db')
        self.c = self.conn.cursor()

    def process_item(self, item, spider):
        self.c.execute("SELECT count(*) FROM rentings WHERE post_id = ?",
                       (item['post_id'],))
        cnt = self.c.fetchone()[0]
        if cnt is not 0:
            return

        # ignore posts that are too old
        if item['post_date'] < 20151101:
            return

        self.c.execute("INSERT into rentings VALUES (?,?,?,?,?,?,?)",
                       (item['post_id'], item['text'], item['url'],
                       item['post_date'], item['post_type'], 0, ''))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
