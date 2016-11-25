#coding:utf-8

import scrapy
from items import CtripHotelItem
from scrapy.http import Request
import time
import codecs
import math
import json
import os
import re

class ctriphotelSpider(scrapy.Spider):
    name = 'ctriphotelSpider'
    allowed_domain = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/international/landmarks/']
    flag = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    file_name = 'ctriphotel' + time.strftime('%Y-%m-%d %H', time.localtime(time.time())) + '.txt'

    def parse(self, response):
        nation_rule = '//ul[@class="nation_list"]/li/strong/a'
        nations = response.xpath(nation_rule)
        if nations != 'None':
            for each_nation in nations:
                each_nation_url = each_nation.xpath('./@href').extract()[0]
                each_nation_id = self.get_data(re.findall(re.compile('(country\d+)'),each_nation_url),0)
                each_nation_name = each_nation.xpath('./text()').extract()[0]
                meta_nation = {'nation':each_nation_name,'nation_id':each_nation_id}
                yield Request(url=each_nation_url+'city/',meta=meta_nation,callback=self.parse_city)

    def parse_city(self,response):
        url_prefix = 'http://hotels.ctrip.com'
        meta_city = response.meta
        city_rule = '//ul[@class="other_city clearfix"]/li/a'
        cities = response.xpath(city_rule)
        if cities:
            for each_city in cities:
                each_city_url = each_city.xpath('./@href').extract()[0]
                each_city_id = self.get_data(re.findall(re.compile('/([a-z]+\d+)/{0,1}'),each_city_url),0)
                each_city_name = each_city.xpath('./text()').extract()[0].replace(u'酒店','')
                meta_city['city'] = each_city_name
                meta_city['city_id'] = each_city_id
                yield Request(url=url_prefix + each_city_url,meta=meta_city,callback=self.parse_page)

    def parse_page(self,response):
        page_meta = response.meta
        start_url = response.url
        page_list_rule = '//div[@class="c_page_list layoutfix"]/a/text()'
        page_list = response.xpath(page_list_rule).extract()
        if page_list:
            max_page = page_list[-1]
            for each_page in range(1,int(max_page)):
                final_url = start_url + '/p' + str(each_page)
                yield Request(url=final_url,meta=page_meta,callback=self.parse_detail)

    def parse_detail(self,response):
        all_room_rule = '//span[@class="total_htl_amount"]/text()[1]'
        not_empty_rule = '//span[@class="total_htl_amount"]/b/text()'
        block_rule = '//div[@class="hotel_list"]/div/div/div/div[@class="hotel_message"]'
        meta = response.meta
        all_room = self.get_data(response.xpath(all_room_rule).extract(),0)
        if all_room != 'None':
            all_room = self.get_data(re.findall(re.compile('\d+'),all_room),0)
        not_empty = self.get_data(response.xpath(not_empty_rule).extract(),0)
        hotel_empty = not_empty + '/' + all_room
        item = CtripHotelItem()
        blocks = response.xpath(block_rule)
        if blocks:
            for each_block in blocks:
                item['hotel_id'] = self.get_data(re.findall(re.compile('/(.*?).html'),self.get_data(each_block.xpath('.//h2[@class="searchresult_name"]/a/@href').extract(),0)),0)
                item['hotel_name'] = self.get_data(each_block.xpath('.//h2[@class="searchresult_name"]/a/text()').extract(),0)
                hotel_score_0 = self.get_data(each_block.xpath('.//a[@class="score_link"]/span/text()').extract(),0)
                hotel_score_1 = self.get_data(each_block.xpath('.//a[@class="score_link"]/text()').extract(),0)
                item['hotel_score'] = u'暂无点评' if hotel_score_0 == hotel_score_1 == 'None' else hotel_score_0+hotel_score_1
                item['hotel_newbook'] = self.get_data(each_block.xpath('.//span[@class="new_book"]/text()').extract(),0)
                item['hotel_RMB'] = self.get_data(each_block.xpath('.//span[@class="hotel_price_pos"]/text()').extract(),0)
                item['hotel_star_desc'] = self.get_data(each_block.xpath('.//h2[@class="searchresult_name"]/span[2]/@title').extract(),0)
                item['hotel_empty'] = hotel_empty
                item['nation_id'] = meta.get('nation_id')
                item['nation_name'] = meta.get('nation')
                item['city_id'] = meta.get('city_id')
                item['city_name'] = meta.get('city')
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
            with codecs.open('/mnt/scrapyPlat/saveFiles/ctrip_hotel/%s' % self.file_name, 'a', 'utf-8') as f: # /mnt/scrapyPlat/saveFiles/
                f.write(tmp)
        except :
            pass

    def get_data(self, list, index):
        if list != None and index < len(list):
            return list[index]
        else:
            return 'None'