# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request

from weibo_scraping.items import WeiboScrapingItem
from weibo_scraping.settings import CONFIG, N_PAGES

XPATH_WB_ENTRY = '//div[@class="c"]'
XPATH_WB_COMMENT = './/a[@class="cc"]/@href'
XPATH_WB_ID = './@id'
XPATH_WB_TEXT = './/span[@class="ctt"]/text()'
XPATH_WB_DATE = './/span[@class="ct"]/text()'

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']


    def __init__(self, nPages=""):
        super(WeiboSpider, self).__init__()
        if not nPages:
            nPages = N_PAGES
        self._read_config(nPages)

    def _read_config(self, nPages):
        # reading config file
        with open(CONFIG, 'r') as f:
            config = json.load(f)

        # start_urls
        agencies = config['agencies']
        self.start_urls = ['http://weibo.cn/u/%s?page=%s' % (agency['id'],
                                                             page) for agency
                           in agencies for page in range(1, int(nPages))]

        # cookies
        self.cookies = config['cookies']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookies, callback=self.parse_weibo)

    def parse_weibo(self, response):
        entries = response.xpath(XPATH_WB_ENTRY)
        for entry in entries:
            try:
                text = entry.xpath(XPATH_WB_TEXT).extract()[0]
            except:
                continue
            else:
                if self.is_valid_text(text):
                    item_id = entry.xpath(XPATH_WB_ID).extract()[0]
                    item_date = \
                        self._get_date(entry.xpath(XPATH_WB_DATE).extract()[0])
                    yield WeiboScrapingItem(text=text, url=response.url,
                                            post_date=item_date,
                                            post_id=item_id)
            '''
            finally:
                urls = entry.xpath(XPATH_WB_COMMENT).extract()
                for url in urls:
                    if 'http' not in url:
                        url = 'http://weibo.cn' + url
                    yield Request(url,
                                  cookies=self.cookies,
                                  callback=self.parse_weibo)
            '''

    def is_valid_text(self, text):
        ptns = [u'求', u'想租', u'急租', u'请问']
        if any(ptn in text for ptn in ptns):
            return True
        else:
            return False

    def _get_date(self, date_text):
        if u'月' in date_text:
            y = '2016'
            m = date_text.split(u'月')[0][-2:]
            d = date_text.split(u'日')[0][-2:]
        else:
            y, m, d = date_text.split()[0].split('-')
        return int(''.join([y, m, d]))
