#coding:utf-8
from scrapy.spider import Spider
from scrapy.http import Request
#from guba.items import GubaItem
from items import GubaItem,GubaListItem
import re
import time
import os

class gubaSpider(Spider):
    '''
    股吧个股沪A 深A 各1004个股票代贴吧的 吧名 和 帖子数
    '''
    name = 'gubaSpider'
    #allowed_domains = ['http://guba.eastmoney.com/']
    start_urls = ['http://guba.eastmoney.com/remenba.aspx?type=1']
    base_url = 'http://guba.eastmoney.com/list,'

    crawl_time = time.strftime('%Y-%m-%d %H %M %S',time.localtime(time.time()))
    crawl_time_save = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    path = 'D:/guba/'
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = str(path) + 'guba_' + str(crawl_time) + '.txt'
    #meta_rule = '//div[@style="display: block;"]/ul/li/a'
    meta_rule = '//div[@style="display: none;"][@class="ngbglistdiv"][position()=2]/ul/li/a | //div[@style="display: block;"]/ul/li/a'
    meta_rule_sh = '//div[@style="display: none;"][@class="ngbglistdiv"][position()=2]/ul/li'
    num_rule = '//span[@class="pagernums"]/@ data-pager'

    def parse(self, response):
        if response:
            try:
                blocks = response.xpath(self.meta_rule)
                #print 'blocks'
                if blocks:
                    for block in blocks:
                        url = self.get_data(block.xpath('./@href').extract(),0)
                        url = self.get_data(url.split(','),1)
                        if url:
                            url =self.base_url + url
                            name = self.get_data(block.xpath('./text()').extract(),0)
                            meta = {'name':name}
                            yield Request(url=url,callback=self.parse_content,meta=meta)
                else:
                    print 'no meta searched'
            except Exception,e:
                print 'err_log',e
        else:
            print 'res is none'

    def parse_content(self,response):
        if response:
            try:
                #print 'num'
                num = self.get_data(response.xpath(self.num_rule).extract(),0)
                num = num.split('|')[1]#re.findall(re.compile('(\d+)'),num)[0]
                #len = len(self.get_data(response.xpath(self.len_rule).extract(),0))
                if num:
                    item = GubaItem()
                    item['stk_code'] = re.findall(re.compile('\((\d+)\)'), response.meta['name'])[0]
                    item['stk_name'] = re.findall(re.compile('\)(.*)'), response.meta['name'])[0]
                    item['num']  = num
                    item['crawl_time'] = self.crawl_time_save
                    #print item['num'].encode('gbk')
                    with open(self.file_name,'a') as f:
                        f.write(item['stk_code'].encode('gbk') + ' ' + item['stk_name'].encode('gbk') + ' ' + item['num'].encode('gbk') + ' ' + item['crawl_time'].encode('gbk') + '\n')
                    #yield item
                else:
                    print 'num got none'
            except Exception,e:
                print 'content parse err_log ',e
        else:
            print 'content res none'

    def get_data(self,list,index):
        if list and index < len(list):
            return list[index]
        else:
            return None
