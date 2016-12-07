#coding:utf-8

import scrapy
from items import EastmoneyItem
from scrapy.http import Request
from extentions.ParseUtil import xpathUtil
import json
import re

class eastmoneySpider(scrapy.Spider):
    name = 'eastmoneySpider'
    allowed_domain = ['eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/center/BKList.html#notion_0_0?sortRule=0']
    dic_name2url = {}

    def parse(self, response):
        blocks = response.xpath('//div[@class="hover-pop col-7 notion"]/ul[@class="ul-col"]/li/a')
        for block in blocks:
            stk_name = xpathUtil.get_data(block.xpath('./span/text()').extract(),0)
            stk_url =  xpathUtil.get_data(block.xpath('./@href').extract(),0)
            stk_url = 'http://quote.eastmoney.com/center/' + stk_url
            meta_fir = {'stk_name':stk_name}
            yield  Request(url=stk_url,meta=meta_fir,callback=self.parse_detail)

    def parse_detail(self, response):
        stk_name = response.meta['stk_name']
        trs = response.xpath('//table[@id="fixed"]/tbody/tr')
        length = len(trs)
        print 'pk'
