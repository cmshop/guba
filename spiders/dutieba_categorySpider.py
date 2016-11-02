#coding:utf-8

import scrapy
from items import DuTiebaItem
from scrapy.http import Request
from urllib import quote
import re
import time
import codecs

class dutieba_categorySpider(scrapy.Spider):
    name = 'dutieba_categorySpider'
    allowed_domain = ['tieba.baidu.com']
    base_url = 'http://tieba.baidu.com'
    file_name = 'du_tieba_' + time.strftime('%Y-%m-%d %H',time.localtime(time.time())) + '.txt'
    #start_urls = ['http://tieba.baidu.com/f?kw=%B4%A5%C3%FE%BB%EC%D2%F4%CC%A82']
    start_urls = ['http://tieba.baidu.com/f/index/forumclass']
                 #'http://tieba.baidu.com/f/index/forumpark?pcn=%C9%CC%D2%B5%B7%FE%CE%F1&pci=0&ct=1',
                  #'http://tieba.baidu.com/f/index/forumpark?pcn=%BD%F0%C8%DA&pci=0&ct=1']

    def parse(self, response):
        #cat_list = [u'客户端网游',u'桌游',u'游戏角色',u'网页版网游',u'手机游戏',u'小游戏',u'单机游戏',u'掌机游戏',u'电视游戏',u'其他游戏及话题']
        cat_list = [(u'游戏',u'客户端网游')]# ,(u'电视剧',u'韩国电视剧'),(u'游戏',u'客户端网游'),(u'体育',u'篮球明星')
        for item in cat_list:
            page_url = 'http://tieba.baidu.com/f/fdir?fd=%s&ie=utf-8&sd=%s'%(item[0],item[1])# quote(item[0].encode('gb2312')),quote(item[1].encode('gb2312'))
            yield Request(url=page_url,meta={'cat_fir':item[0],'cat_sec':item[1]},callback=self.parse_cat_fir)

    def parse_cat_fir(self,resposne):
        cat_sec_url_rule = '//a[@target="_self"]'
        cat_sec_url = {}
        cat_sec_url[resposne.meta['cat_sec']] = resposne.url

        cat_sec_urls = resposne.xpath(cat_sec_url_rule)
        if cat_sec_urls:
            for each_cat_sec_url in cat_sec_urls:
                cat_sec_url_name = self.get_data(each_cat_sec_url.xpath('./text()').extract(),0)
                cat_sec_url_href = self.get_data(each_cat_sec_url.xpath('./@href').extract(),0)
                cat_sec_url[cat_sec_url_name] = cat_sec_url_href
        #print len(cat_sec_url)
        for key in cat_sec_url.keys():
            if cat_sec_url[key] != 'None':
                yield Request(url=('http://tieba.baidu.com' if 'http' not in cat_sec_url[key] else '') +cat_sec_url[key],meta={'cat_fir':resposne.meta['cat_fir'],'cat_sec':key},callback=self.parse_cat)

    def parse_cat(self,response):
        try:
            max_page_rule = u'<a href=([^<>]*?)>\u5c3e\u9875</a>'.encode('gb18030')
            max_page_url = self.get_data(re.findall(re.compile(max_page_rule),response.body),0)
            list_url = response.url.split('pn=')[0] + '&pn='
            if max_page_url:
                max_page = self.get_data(re.findall(re.compile('pn=(\d+)'),max_page_url),0)
                if max_page != 'None':
                    for i in range(1,int(max_page)+1):
                        yield Request(url=list_url+str(i),meta=response.meta,callback=self.parse_list)
                else:
                    print 'max_page not found...'
            else:
                print 'max_page not found...'
        except Exception,e:
            print 'parse_cat err: ',str(e)[:50]

    def parse_list(self,resposne):
        try:
            title_rule = '//td/a[@target="_blank"]'
            titles = resposne.xpath(title_rule)
            for title in titles:
                title_name = self.get_data(title.xpath('./text()').extract(),0)
                title_url = self.get_data(title.xpath('./@href').extract(),0)
                meta_list = resposne.meta
                meta_list['title_name'] = title_name
                if title_url is not None:
                    yield Request(url=title_url,meta=meta_list,callback=self.parse_detail)
        except Exception,e:
            print 'parse_list err: ',str(e)[:50]

    def parse_detail(self, response):
        try:
            html = response.body
            #title = re.findall(re.compile('<span class="card_infoNum">(.*?)</span>'),html) #'card_title_fname.*?>(.*?)</a>'
            attention_num = self.get_data(re.findall(re.compile('<span class="card_menNum">(.*?)</span>'),html),0)
            article_num = self.get_data(re.findall(re.compile('<span class="card_infoNum">(.*?)</span>'),html),0)
            item = DuTiebaItem()
            item['cat_fir'] = response.meta['cat_fir']
            item['cat_sec'] = response.meta['cat_sec']
            item['flag'] = str(time.strftime('%Y-%m-%d', time.localtime(time.time()))).decode('utf-8')
            item['title'] = response.meta['title_name']
            item['attention_num'] = attention_num.decode('utf-8')
            item['article_num'] = article_num.decode('utf-8')

            #yield item
            with codecs.open('D:/%s'% self.file_name,'a','utf-8') as f:
                f.write(item['cat_fir'] + '&/#' + item['cat_sec'] + '&/#' + item['title'] + '&/#' +
                        item['attention_num'] + '&/#' + item['article_num']+'&/#'+item['flag']+ '\n')
        except Exception,e:
            print 'parse detail err: ',str(e)[:50]

    def get_data(self,list,index):
        if list != None and index < len(list):
            return list[index]
        else:
            return 'None'
