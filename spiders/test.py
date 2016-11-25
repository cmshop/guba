#coding:utf-8

import scrapy
from items import AutoHomePriceItem
from scrapy.http import Request

class test(scrapy.Spider):
    name = 'test'
    allowed_domain = ['autohome.com.cn']
    start_urls = ['http://mall.autohome.com.cn/index.html']

    def parse(self, response):
        url = response.url
        print 'ok'