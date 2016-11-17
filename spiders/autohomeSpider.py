#coding:utf-8

import scrapy
from items import AutoHomeItem
from scrapy.http import Request
import re
import time
import codecs
import math

class autohomeSpider(scrapy.Spider):
    name = 'autohomeSpider'
    allowed_domain = ['autohome.com.cn']
    flag = time.strftime('%Y-%m-%d_%H', time.localtime(time.time()))
    start_urls = ['http://mall.autohome.com.cn/index.html']
    prefix_url = 'http://mall.autohome.com.cn'
    file_name = 'autohome' + time.strftime('%Y-%m-%d %H', time.localtime(time.time())) + '.txt'

    def parse(self, response):
        cat_urls =  ['http://mall.autohome.com.cn/list/2-500100-0-0-0-0-0-0-0-1.html?factoryId=0&minPrice=-1&maxPrice=-1&stageTag=0&importTag=0&double11Tag=0&prefix=&dataSource=',
                  'http://mall.autohome.com.cn/list/1-110100-0-0-0-0-0-0-0-1.html?factoryId=0&minPrice=-1&maxPrice=-1&stageTag=0&importTag=0&double11Tag=0&prefix=&dataSource=',
                  'http://mall.autohome.com.cn/list/3-110100-0-0-0-0-0-0-0-1.html?factoryId=0&minPrice=-1&maxPrice=-1&stageTag=0&importTag=0&double11Tag=0&prefix=&dataSource=']
        for cat_url in cat_urls:
            yield Request(url=cat_url,callback=self.parse_address)

    def parse_address(self,response):
        address_rule = '//div[@class="selectcity-content"]/dl[@class="fn-clear"]/dd/a/@id'
        address = response.xpath(address_rule).extract()
        if isinstance(address,list) and len(address) > 1:
            address = address[1:]
            for address_code in address:
                final_url = re.sub(re.compile('\d{6}'),address_code,response.url)
                yield Request(url=final_url,callback=self.parse_page_plan_1)
        else:
            print 'parse address err!'

    #方案一，通过给定一个比较大的页码，找到真实最大页
    def parse_page_plan_0(self,response):
        max_page_url_temp = re.sub(re.compile('-\d.html'),'-1000.html',response.url)
        yield Request(url=max_page_url_temp,callback=self.parse_page_plan_0_1)

    def parse_page_plan_0_1(self,response):
        max_page_rule = '//span[@class="pager-pageindex"]/a/@href'
        max_page_url = self.prefix_url + response.xpath(max_page_rule).extract()[-1]
        yield Request(url=max_page_url,callback=self.parse_detail)

    # 方案二，通过总商品数和每一页的商品数量做除法，向上取整的到最大页
    def parse_page_plan_1(self,response):
        product_nums_rule = '//span[@class="condition-total"]/text()'
        product_nums = self.get_data(response.xpath(product_nums_rule).extract(),0)
        if product_nums != 'None':
            product_num = self.get_data(re.findall(re.compile('\d+'),product_nums),0)
            max_page = int(math.ceil(int(product_num)/24))
            for page_num in range(max_page):
                final_url = re.sub('-\d.html','-%s.html'%str(page_num+1),response.url)
                yield Request(url=final_url,callback=self.parse_detail)

    def parse_detail(self,response):
        try:
            blocks_rule = '//div[@class="list"]/ul/li'
            blocks = response.xpath(blocks_rule)
            item = AutoHomeItem()
            cat_name = self.get_data(response.xpath('//li[@class="tab-item current"]/a/text()').extract(),0)
            address = self.get_data(response.xpath('//span[@id="btnSelectCity"]/text()[1]').extract(),0)
            if blocks:
                for block in blocks:
                    item['cat_id'] = self.get_data(re.findall(re.compile('list/(\d+)-'),response.url),0)
                    item['cat_name'] = cat_name
                    item['address'] = address.replace('\n','').strip()
                    item['product_price_current'] =self.get_data(block.xpath('.//div[@class="carbox-info"]/span/text()').extract(),0)
                    item['product_price_origion'] = self.get_data(block.xpath('.//del/text()').extract(),0)
                    item['product_title'] = self.get_data(block.xpath('.//div[@class="carbox-title"]/@title').extract(),0)
                    item['sales'] = self.get_data(block.xpath('.//div[@class="carbox-number"]/span/text()').extract(),0)
                    item['product_id'] = self.get_data(re.findall(re.compile('detail/(.*?).html'),self.get_data(block.xpath('.//a/@href').extract(),0)),0)
                    item['flag'] = self.flag
                    item['crawler_time'] = str(time.time())
                    self.write2file(item)
            else:
                print 'this page has no blocks! %s'%response.url
        except Exception,e:
            print 'parse_detail err: ',str(e)

    def write2file(self,dic):
        tmp = ''
        for index,value in enumerate(dic.keys()):
            if index != len(dic.keys())-1:
                tmp += (dic[value].decode() if isinstance(dic[value],str) else dic[value]).replace('\n','')+'&/#'
            else:
                tmp  += dic[value].replace('\n','') + '\n'
        try:
            with codecs.open('D:/%s' % self.file_name, 'a', 'utf-8') as f:
                f.write(tmp)
        except :
            pass

    def get_data(self, list, index):
        if list != None and index < len(list):
            return list[index]
        else:
            return 'None'

