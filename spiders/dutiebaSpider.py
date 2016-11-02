#coding:utf-8

import scrapy
from items import DuTiebaItem
from scrapy.http import Request
from urllib import quote
import re
import time
from DBlib.MySQLdb import MySql

class dutiebaSpider(scrapy.Spider):
    name = 'dutiebaSpider'
    allowed_domain = ['tieba.baidu.com']
    base_url = 'http://tieba.baidu.com'
    file_name = 'du_tieba_' + time.strftime('%Y-%m-%d %H',time.localtime(time.time())) + '.txt'
    start_urls = ['http://tieba.baidu.com/f/index/forumclass']
                 #'http://tieba.baidu.com/f/index/forumpark?pcn=%C9%CC%D2%B5%B7%FE%CE%F1&pci=0&ct=1',
                  #'http://tieba.baidu.com/f/index/forumpark?pcn=%BD%F0%C8%DA&pci=0&ct=1']

    def parse_detail(self, response):
        #max_page = 30
        #max_page_bool = False
        item = DuTiebaItem()
        cat_fir = self.get_data(response.xpath('//h3/a/text()').extract(),0)
        cat_sec = self.get_data(response.xpath('//a[@class="cur_class"]/text()').extract(),0)
        blocks = response.xpath('//div[@class="ba_content"]')
        #if max_page_bool == False:
            #max_page = int(self.get_data(response.selector.re(u'<a href=[^<>]*?pn=(.*?)">\u5c3e\u9875</a>'),0))
            #max_page_bool = True
        if blocks:
            #print len(blocks),'*'*10
            for block in blocks:
                #print block.extract().encode('gbk')
                item['cat_fir'] = cat_fir
                item['cat_sec'] = cat_sec
                item['title'] = self.get_data(block.xpath('.//p[@class="ba_name"]/text()').extract(),0)
                item['attention_num'] = self.get_data(block.xpath('.//span[@class="ba_m_num"]/text()').extract(),0)
                item['article_num'] = self.get_data(block.xpath('.//span[@class="ba_p_num"]/text()').extract(),0)
                item['flag'] = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
                #yield item
                with open('D:/%s'% self.file_name,'a') as f:
                    f.write(item['cat_fir'].encode('gbk') + ' ' + item['cat_sec'].encode('gbk') + ' ' + item['title'].encode('gbk') + ' ' + item['attention_num'].encode('gbk') + ' ' + item['article_num'].encode('gbk') + '\n')

    def parse(self, response):
        #print 'ok'
        #self.parse_detail(response)
        cat_list = [u'电影',u'电视剧',u'金融',u'体育',u'电视节目',u'游戏',u'工农业产品',u'生活用品',u'商业服务',u'电脑数码',u'教育培训',u'企业',u'科学技术']
        for item in cat_list:
            #for i in range(20,self.max_page):
            #    print 'page num:',i
                #page_url = response.url.split('pn=')[0] + 'ct=%s'%str(i)
            page_url = 'http://tieba.baidu.com/f/index/forumpark?cn=&ci=0&pcn=%s&pci=0&ct=1&st=popular&pn=1'%(quote(item.encode('gb2312')))
            print page_url
            yield Request(url=page_url,callback=self.parse_cat)

    def parse_cat(self,response):
        blocks = response.xpath('//ul[@class="class_list clearfix"]/li/a/@href').extract()
        max_page = self.get_data(response.xpath('//div[@class="pagination"]/a[last()]/@href').extract(),0)
        if max_page != None:
            max_page = re.findall(re.compile('&pn=(.*?)$'),max_page)[0]
            max_page = int(max_page)
        else:
            max_page = 1
        if blocks:
            for block in blocks:
                subdetail_url = self.base_url + block.split('&pn=')[0]
                for i in range(1,max_page+1):
                    detail_url = subdetail_url + '&pn=%s'%str(i)
                    yield Request(url=detail_url,callback=self.parse_detail)


    def get_data(self,list,index):
        if list != None and index < len(list):
            return list[index]
        else:
            return None
