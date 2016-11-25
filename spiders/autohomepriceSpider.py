#coding:utf-8

import scrapy
from items import AutoHomePriceItem
from scrapy.http import Request
import time
import codecs
import math
import json
import os
import re

class autohomepriceSpider(scrapy.Spider):
    name = 'autohomepriceSpider'
    allowed_domain = ['autohome.com.cn']
    # download_delay = 5
    flag = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    start_urls = ['http://mall.autohome.com.cn/index.html']
    prefix_url = 'http://mall.autohome.com.cn'
    file_name = 'autohome_price' + time.strftime('%Y-%m-%d %H', time.localtime(time.time())) + '.txt'
    read_file_regex = 'autohome'+ time.strftime('%Y-%m-%d', time.localtime(time.time()))
    ajax_url = 'http://mall.autohome.com.cn/http/data.html?data[_host]=http://mall.api.autohome.com.cn/item/price/getPriceForList&data[_appid]=mall&data[itemIds]=%s&data[platform]=1&data[isReturnOtherPlatform]=false'

    def parse(self, response):
        items = []
        file_path = '/mnt/scrapyPlat/saveFiles/'
        files_dir = os.listdir(file_path)
        for file_name in files_dir:
            if self.get_data(re.findall(re.compile(self.read_file_regex),file_name),0) != 'None':
                try:
                    with open(file_path+file_name) as f:
                        items = [x.split('\n')[0].split('&/#')[2].split('-')[0] for x in f if x.split('\n')[0].split('&/#')[4]=='2']
                except Exception,e:
                    print 'read file err: ',str(e)
                break
        if len(items) != 0:
            print 'all items num: %s'%str(len(items))
            items = list(set(items))
            print 'filtered items num: %s' % str(len(items))
            num = len(items)
            threshold = 24
            flag = int(math.ceil(num / float(threshold)))
            for i in range(flag):
                itemIds = ','.join(items[i * threshold:(i + 1) * threshold])
                ajax_url_final = self.ajax_url % itemIds
                yield Request(url=ajax_url_final,callback=self.parse_detail)

    def parse_detail(self,response):
        ajax_data = json.loads(response.body)
        item = AutoHomePriceItem()
        for value in ajax_data.get('result'):
            item['product_price_current'] = str(value['item']['price'])
            item['product_id'] = str(value['item']['itemId'])
            item['flag'] = self.flag
            item['crawler_time'] = str(time.time())
            self.write2file(item)

    def write2file(self,dic):
        tmp = ''
        for index,value in enumerate(dic.keys()):
            if index != len(dic.keys())-1:
                tmp += (dic[value].decode() if isinstance(dic[value],str) else dic[value]).replace('\n','')+'&/#'
            else:
                tmp  += dic[value].replace('\n','') + '\n'
        try:
            with codecs.open('/mnt/scrapyPlat/saveFiles/autohome_mall/%s' % self.file_name, 'a', 'utf-8') as f: # /mnt/scrapyPlat/saveFiles/ /mnt/scrapyPlat/saveFiles/autohome_mall
                f.write(tmp)
        except :
            pass

    def get_data(self, list, index):
        if list != None and index < len(list):
            return list[index]
        else:
            return 'None'