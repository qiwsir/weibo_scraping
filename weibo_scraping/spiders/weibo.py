# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request

from weibo_scraping.items import WeiboScrapingItem
from weibo_scraping.settings import CONFIG

XPATH_WB_ENTRY = '//div[@class="c"]'
XPATH_WB_TEXT = './/span[@class="ctt"]/text()'
XPATH_WB_COMMENT = './/a[@class="cc"]/@href'

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']

    # reading config file
    with open(CONFIG, 'r') as f:
        config = json.load(f)

    # start_urls
    user_ids = config['user_ids']
    start_urls = ['http://weibo.cn/u/' + uid for uid in user_ids]

    # cookies
    cookies = config['cookies']

    # def make_requests_from_url(self, url):
    #     request = super(WeiboSpider, self).make_requests_from_url(url)
    #     for k in self.cookies:
    #         request.cookies[k] = self.cookies[k]
    #     return request

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookies, callback=self.parse_weibo)

    def parse_weibo(self, response):
        # print '='*20
        # print response.headers
        # print '='*20
        entries = response.xpath(XPATH_WB_ENTRY)
        for entry in entries:
            try:
                text = entry.xpath(XPATH_WB_TEXT).extract()[0]
            except:
                continue
            else:
                if self.is_valid_text(text):
                    yield WeiboScrapingItem(text=text, url=response.url)
            finally:
                urls = entry.xpath(XPATH_WB_COMMENT).extract()
                for url in urls:
                    if 'http' not in url:
                        url = 'http://weibo.cn' + url
                    yield Request(url,
                                  cookies=self.cookies,
                                  callback=self.parse_weibo)

    def is_valid_text(self, text):
        ptns = [u'求', u'想租', u'急租', u'请问']
        if any(ptn in text for ptn in ptns):
            return True
