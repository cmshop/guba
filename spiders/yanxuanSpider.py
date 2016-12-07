#coding:utf-8

import scrapy
from items import YanXuanItem
from scrapy.http import Request
import re
import time
import codecs

class yanxuanSpider(scrapy.Spider):
    name = 'yanxuanSpider'
    allowed_domain = ['you.163.com']
    file_name = 'yanxuan' + time.strftime('%Y-%m-%d %H', time.localtime(time.time())) + '.txt'
    flag = time.strftime('%Y-%m-%d_%H', time.localtime(time.time()))
    #start_urls = ['http://you.163.com/?s_stat_area=nav_1&_stat_referer=index']
    start_urls = ['http://you.163.com/item/list?categoryId=1005000&_stat_area=nav_2&_stat_referer=index#sortType=2&descSorted=true&subCategoryId=1005000']

    def parse(self, response):
        with open('files/yanxuan_url_list', 'r') as f:
            yanxuan_url_list = [x.split('\n')[0] for x in f]
        for item in yanxuan_url_list:
            yield Request(url=item,callback=self.parse_detail)

    def parse_detail(self,response):
        blocks_rule = '//div[@class="m-product product-s j-product"]'
        blocks = response.xpath(blocks_rule)
        if blocks != 'None':
            for block in blocks:
                product_url = self.get_data(block.xpath('.//div[@class="hd"]/a/@href').extract(), 0)
                full_url = 'http://you.163.com' + product_url
                yield Request(url=full_url,callback=self.get_num) # ,meta={'item':item}

    def get_num(self,response):
        item = YanXuanItem()
        try:
            item['flag'] = self.flag
            cat_url = self.get_data(response.xpath('//div[@class="m-crumbs"]/a[2]/@href').extract(),0)
            item['cat_id'] = self.get_data(re.findall(re.compile('categoryId=(\d+)'),cat_url),0)  if cat_url != 'None' else 'None'
            item['cat_name'] = self.get_data(response.xpath('//div[@class="m-crumbs"]/a[2]/text()').extract(),0)
            item['product_id'] = self.get_data(re.findall(re.compile('id=(\d+)&'),response.url),0)
            item['product_title'] = self.get_data(response.xpath('//span[@class="z-cur"]/text()').extract(),0)
            item['product_price_current'] = self.get_data(response.xpath('//span[@class="num j-retail-price"]/text()').extract(),0)
            item['crawler_time'] = str(time.time())
            num = self.get_data(response.xpath('//span[@class="num"]/text()').extract(),0)
            if num != 'None':
                num = self.get_data(re.findall(re.compile('(\d+)'),num),0)
            item['product_comment_num'] = num
            self.write2file(item)
        except:
            pass

    def write2file(self,dic):
        tmp = ''
        for index,value in enumerate(dic.keys()):
            if index != len(dic.keys())-1:
                tmp += (dic[value].decode() if isinstance(dic[value],str) else dic[value]).replace('\n','')+'&/#'
            else:
                tmp  += dic[value].replace('\n','') + '\n'
        with codecs.open('D:/%s' % self.file_name, 'a', 'utf-8') as f:
            f.write(tmp)

    def get_data(self, list, index):
        if list != None and index < len(list):
            return list[index]
        else:
            return 'None'