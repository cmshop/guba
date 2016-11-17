#coding:utf-8

import scrapy
from items import KalLaItem
from scrapy.http import Request
import re
import time
import codecs

class kaolaSpider(scrapy.Spider):
    name = 'kaolaSpider'
    allowed_domain = ['kaola.com']
    file_name = 'kaola' + time.strftime('%Y-%m-%d %H', time.localtime(time.time())) + '.txt'
    start_urls = ['http://www.kaola.com/']
    flag = time.strftime('%Y-%m-%d_%H',time.localtime(time.time()))
    list_url = '?pageSize=60&pageNo=%s&sortfield=0&isStock=false&isSelfProduct=false&isPromote=false&isDesc=true&b=&proIds=&source=false&country=&isNavigation=0&lowerPrice=-1&upperPrice=-1'

    def parse(self, response):
        with open('files/kaola_url_list', 'r') as f:
            kaola_url_list = [x.split('\n')[0] for x in f]
        for item in kaola_url_list:
            yield Request(url=item,callback=self.parse_max)
    def parse_max(self,response):
        max_page = self.get_data(response.xpath('//div[@class="simplePage"]/span/text()').extract(),0)
        if max_page != 'None':
            max_page = self.get_data(re.findall(re.compile('/(\d+)'),max_page),0)
            for i in range(1,int(max_page)+1):
                page_url = response.url.split('?')[0] + self.list_url%str(i)
                yield Request(url=page_url,callback=self.parse_list)

    def parse_list(self,response):
        try:
            item = KalLaItem()
            cat_id = re.findall(re.compile('category/(\d+).htm'), response.url)[0]
            cat_name = self.get_data(response.xpath('//p[@class="total"]/a[2]/text()').extract(), 0)
            block_rule = '//li[@class="goods"]'
            blocks = response.xpath(block_rule)
            if blocks != None:
                for block in blocks:
                    item['cat_id'] = cat_id
                    item['cat_name'] = cat_name
                    item['flag'] = self.flag
                    item['crawler_time'] = str(time.time())
                    product_id = self.get_data(block.xpath('.//div[@class="img"]/a[@target="_blank"]/@href').extract(), 0)
                    if product_id:
                        product_id = re.findall(re.compile('product/(\d+).html'), product_id)[0]
                    item['product_id'] = product_id
                    item['product_title'] = self.get_data(
                        block.xpath('.//div[@class="img"]/a[@target="_blank"]/@title').extract(), 0)
                    item['product_price_origion'] = self.get_data(
                        block.xpath('.//span[@class="marketprice"]/del/text()').extract(), 0)
                    item['product_price_current'] = self.get_data(block.xpath('.//span[@class="cur"]/text()').extract(), 0)
                    item['product_comment_num'] = self.get_data(
                        block.xpath('.//p[@class="goodsinfo clearfix"]/a/text()').extract(), 0)
                    item['product_selfflag'] = self.get_data(
                        block.xpath('.//p[@class="selfflag"]/span/text() | .//p[@class="selfflag"]/a/text()').extract(), 0)
                    # yield  item
                    # with codecs.open('D:/%s' % self.file_name, 'a', 'utf-8') as f:
                    #     f.write(item['cat_id']+'&/#'+item['cat_name']+'&/#'+item['flag']+'&/#'+item['crawler_time']+'&/#'+
                    #             item['product_id']+'&/#'+item['product_title']+'&/#'+)
                    self.write2file(item)

        except Exception,e:
            print 'parse_list err: ',str(e)

    def write2file(self,dic):
        tmp = ''
        for index,value in enumerate(dic.keys()):
            if index != len(dic.keys())-1:
                tmp += (dic[value].decode() if isinstance(dic[value],str) else dic[value])+'&/#'
            else:
                tmp  += dic[value] + '\n'
        with codecs.open('D:/%s' % self.file_name, 'a', 'utf-8') as f:
            f.write(tmp)

    def get_data(self, list, index):
        if list != None and index < len(list):
            return list[index]
        else:
            return 'None'
