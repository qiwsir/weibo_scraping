# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request

from weibo_scraping.items import WeiboScrapingItem
from weibo_scraping.settings import CONFIG, N_PAGES, POST, COMMENT

XPATH_WB_POST = '//div[@class="c" and starts-with(@id, "M")]'
XPATH_WB_COMMENT = '//div[@class="c" and starts-with(@id, "C")]'
XPATH_WB_COMMENT_REF = './/a[@class="cc"]/@href'
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
        """read config file which contains agencies to scrape and tags to
        search"""
        # sanity check
        nPages = int(nPages)
        nPages = max(nPages, 2)
        nPages = min(nPages, 50)

        # reading config file
        with open(CONFIG, 'r') as f:
            config = json.load(f)

        # homepages of agencies
        agencies = config['agencies']
        self.start_urls = ['http://weibo.cn/u/%s?page=%s' %
                           (agency['id'], page) for agency in agencies
                           for page in range(1, nPages)]

        # search for posts that @agencies
        # http://weibo.cn/search/mblog?hideSearchFrame=&keyword=关键词&page=2
        self.start_urls += \
            ['http://weibo.cn/search/mblog?hideSearchFrame=&keyword=@%s&page=%s'
             % (agency['name'], page) for agency in agencies
             for page in range(1, int(nPages))]

        # search for posts that have tags
        self.start_urls += \
            ['http://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&page=%s'
             % (keyword, page) for keyword in config['tags']
             for page in range(1, int(nPages))]

        # cookies
        self.cookies = config['cookies']

    def start_requests(self):
        """overwrite start_request to use cookies"""
        for url in self.start_urls:
            yield Request(url, cookies=self.cookies, callback=self.parse_weibo)

    def parse_weibo(self, response):
        entries = response.xpath(XPATH_WB_POST)
        for entry in entries:
            text = ''.join(entry.xpath(XPATH_WB_TEXT).extract())

            # case1: msgs from agencies are mostly ads
            if self.is_relevant_agency_ad(text):
                urls = entry.xpath(XPATH_WB_COMMENT_REF).extract()
                # reposted msgs may have >1 urls (original and repost)
                for url in urls:
                    if 'http' not in url:
                        url = 'http://weibo.cn' + url
                    yield Request(url,
                                  cookies=self.cookies,
                                  callback=self.parse_tenant_comments)

            # case2: msgs that are reposted by agencies can be from tenant
            if self.is_relevant_tenant_post(text):
                item_id = entry.xpath(XPATH_WB_ID).extract()[0]
                item_date = \
                    self._get_date(entry.xpath(XPATH_WB_DATE).extract()[0])
                yield WeiboScrapingItem(text=text, url=response.url,
                                        post_date=item_date,
                                        post_id=item_id,
                                        post_type=POST)

    def parse_tenant_comments(self, response):
        """scrape all comments by potential tenants seeking for
        accommodation. request should be initiated by following a link of
        agency ad (case1 in `parse_weibo`)"""
        entries = response.xpath(XPATH_WB_COMMENT)
        for entry in entries:
            text = ''.join(entry.xpath(XPATH_WB_TEXT).extract())
            item_id = entry.xpath(XPATH_WB_ID).extract()[0]
            item_date = \
                self._get_date(entry.xpath(XPATH_WB_DATE).extract()[0])
            yield WeiboScrapingItem(text=text, url=response.url,
                                    post_date=item_date,
                                    post_id=item_id,
                                    post_type=COMMENT)

    def is_relevant_tenant_post(self, text):
        """try to identify posts that are seeking for a place"""
        # ignore posts for other cities
        if self._is_other_city(text):
            return False

        # tenants posted ads contains phrases
        if (any(ptn in text for ptn in [u'求租', u'想租', u'急租'])):
            return True
        # tenants posted ads contains combinations of characters
        elif any(ptn in text for ptn in [u'房', u'室', u'室']) and \
            any(ptn in text for ptn in [u'求', u'找']):
            return True
        else:
            return False

    def is_relevant_agency_ad(self, text):
        """try to identify ads that are renting rooms out"""
        # ignore posts for other cities
        if self._is_other_city(text):
            return False

        if any(ptn in text for ptn in
               [u'转租', u'招租', u'超美', u'超大', u'超好', u'预约',
                u'预约', u'看房', u'出租']):
            return True
        else:
            return False

    def _is_other_city(self,text):
        """return True if not in London"""
        if any(ptn in text for ptn in
               [u'考文垂', u'爱丁堡', u'利物浦', u'诺丁汉', u'伯明翰',
                u'曼彻斯特', u'谢菲尔']):
            return True
        else:
            return False

    def _get_date(self, date_text):
        """convert strings like "2015-03-10", "1月8号" to integers"""
        if u'月' in date_text:
            y = '2016'
            m = date_text.split(u'月')[0][-2:]
            d = date_text.split(u'日')[0][-2:]
        else:
            y, m, d = date_text.split()[0].split('-')
        return int(''.join([y, m, d]))
