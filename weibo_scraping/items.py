# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    post_date = scrapy.Field()
    post_id = scrapy.Field()
    post_type = scrapy.Field()  # 0 is post, 1 is comment - see settings.py
