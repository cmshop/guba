#coding:utf-8

from items import XueqiuItem
from scrapy.spider import Spider
from scrapy.http import Request
import re
import json
import os,time
from cleaner.timeformat import TimeFormat
from settings import ROOT
from random import randint

class xueqiuSpider(Spider):
    name = 'xueqiuSpider'
    #allowed_domains = ['']
    start_urls = ['http://xueqiu.com/']
    codes = []
    base_url_0 = 'http://xueqiu.com/statuses/search.json?count=20&comment=0&symbol='#SZ300104&hl=0&source=user&sort=time&page=1'
    base_url_1 = '&hl=0&source=user&sort=time&page='

    crawl_time = time.strftime('%Y-%m-%d_%H', time.localtime(time.time()))
    crawl_time_stamp = time.time()
    deadline = time.strftime('%Y-%m-%d %H', time.localtime(time.time() - 60*60)) + ':00:00'
    endtime = time.strftime('%Y-%m-%d %H', time.localtime(time.time())) + ':00:00'
    #deadline = '2016-06-01 00:00:00'
    page_dic = {50:None,30:None,80:None,20:None,10:None,3:None}
    download_delay = randint(2,5)*0.1
    path = ROOT + 'xueqiu/' + str(crawl_time) + '/'
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = str(path) + 'xueqiu_' + str(crawl_time) + '.txt'


    def parse(self, response):
        with open('C:/Users/xingweiyong/spiders/guba/guba/guba/files/guba.txt', 'r') as f:
            codes = [self.get_code(x) for x in f]
        #codes = [('SZ300104','乐视')] # ,('SZ000001',u'平安银行')
        #codes = [('SZ300218','安利股份')]
        #codes = codes[0:5]

        for item in codes:
            self.page_dic = {50:None,30:None,20:None,10:None,3:None}

            # for i in self.page_dic.keys():
            #     url = self.base_url_0 + item[0] + self.base_url_1 + str(i)
            #     meta_temp = {'max':i,'item':item[0],'item_name':item[1]}
            #     yield Request(url=url,meta=meta_temp,callback=self.get_max_page)

            max_page = 2
            for i in range(1,max_page+1):
                url = self.base_url_0 + item[0] + self.base_url_1 + str(i)
                meta_temp = {'max': i, 'item': item[0], 'item_name': item[1]}
                #page += 1
                yield Request(url=url,meta=meta_temp ,callback=self.parse_json)


    def get_max_page(self,response):
        max_page = 100
        item = response.meta['item']
        item_name = response.meta['item_name']
        dic_str = json.loads(response.body)
        dic_str = dic_str['list']
        if len(dic_str) != 0:
            timeBefore = dic_str[0].get('timeBefore', 'none')
            timeBefore = TimeFormat(timeBefore, self.crawl_time_stamp).conver2Format()

            if timeBefore < self.deadline:
                self.page_dic[response.meta['max']] = True
            else:
                self.page_dic[response.meta['max']] = False
        else:
            self.page_dic[response.meta['max']] = False

        if None not in self.page_dic.values():
            list_temp = self.page_dic.keys()
            list_temp.sort()
            dic = self.page_dic
            for value in list_temp:
                if self.page_dic[value] == True:
                    max_page = value
                    #max_page = 100 #special
                    for i in range(1, max_page+1):
                        url = self.base_url_0 + str(item) + self.base_url_1 + str(i)
                        meta_temp = {'item':item,'item_name':item_name}
                        yield Request(url=url,meta=meta_temp, callback=self.parse_json)
                    break
            '''
            if True not in self.page_dic.values():
                max_page = 100
                for i in range(1, max_page + 1):
                    url = self.base_url_0 + str(item) + self.base_url_1 + str(i)
                    meta_temp = {'item': item, 'item_name': item_name}
                    yield Request(url=url, meta=meta_temp, callback=self.parse_json)
            '''
    def parse_json(self,response):
        try:
            dic_str = json.loads(response.body)
            dic_str = dic_str['list']
            item_code = response.meta['item']
            item_name = response.meta['item_name']
            for value in dic_str:
                comm_id = value.get('id','none')
                text = value.get('text','none')
                timeBefore = value.get('timeBefore','none')
                reply_count = value.get('reply_count','none')

                retweet_count = value.get('retweet_count', 'none')
                reward_count = value.get('reward_count', 'none')
                fav_count = value.get('fav_count', 'none')
                user_id = value.get('user_id', 'none')
                retweeted_status = 1 if value['retweeted_status'] != None else 0

                timeBefore = TimeFormat(timeBefore,self.crawl_time_stamp).conver2Format()
                if timeBefore and value['retweeted_status'] == None:

                    item = XueqiuItem()
                    item['comm_id'] = comm_id
                    item['item'] = item_code
                    item['item_name'] = item_name
                    item['text'] = text
                    item['timeBefore'] = str(timeBefore)
                    item['reply_count'] = str(reply_count)
                    item['retweet_count'] = str(retweet_count)
                    item['reward_count'] = str(reward_count)
                    item['fav_count'] = str(fav_count)
                    item['user_id'] = str(user_id)
                    item['crawl_time'] = self.crawl_time
                    item['retweeted_status'] = retweeted_status

                    if timeBefore > self.deadline and timeBefore < self.endtime:
                        with open(self.file_name,'a') as f:
                            f.write(str(item['comm_id']) + ' ' + item['item'] + ' ' + item['item_name']+ ' ' + item['timeBefore'] + ' ' + item['reply_count'].encode( 'gbk') + '\n')
                        '''
                        with open(self.file_name,'a') as f:
                            f.write(str(item['comm_id']) + '&/#' +
                                    item['item'] + '&/#' +
                                    item['item_name'] +'&/#'+
                                    item[ 'user_id']+ '&/#' +
                                    item['timeBefore'] + '&/#' +
                                    item['reply_count'].encode('gbk') +'&/#'+
                                    item['retweet_count'].encode('gbk')+ '&/#' +
                                    item['reward_count'].encode('gbk')+'&/#'+
                                    item['fav_count'].encode('gbk')+ '&/#' +
                                    item['crawl_time']+'&/#'+
                                    str(item['retweeted_status'])+ '&/#'+
                                    item['text'].encode('gbk','ignore')  + '\n') #  + ' ' + item['text'].encode('gbk','ignore') + ' ' + item['text'].encode('gbk','ignore')
                            #yield item

                        with open(self.file_name, 'a') as f:
                            f.write(
                                str(item['comm_id']) + ' ' + item['item'] + ' ' + item['item_name'] + ' ' +
                                item[ 'user_id'] + ' ' + item['timeBefore'] + ' ' + item['reply_count'].encode( 'gbk') + ' ' +
                                item['retweet_count'].encode('gbk') + ' ' + item['reward_count'].encode('gbk') + ' ' +
                                item['fav_count'].encode('gbk') + ' ' + item['crawl_time'] + ' ' +
                                item['retweeted_status'] + ' '+ item['text'].encode('gbk') + '\n')
                        '''
        except Exception,e:
            print '需要打码...',e
            #raw_input('> 请在页面输入验证码，按任意键继续: ')


    def get_code(self,content):
        temp = self.get_data(re.findall(re.compile('\((.*?)\)'),content),0)
        temp_name = self.get_data(re.findall(re.compile('\)(.*?)$'),content),0)
        if temp:
            '''
            if temp[0] == str(6):
                return ('SH' + temp,temp_name)
            elif temp[0] == str(0) or temp[0] == str(3):
                return ('SZ' + temp,temp_name)
            else:
                print 'not 0/3/6...'
                return None
           '''
            return (temp,temp_name)
        else:
            print 'get code err'
            return None

    def get_data(self,list,index):
        if list and index < len(list):
            return list[index]
        else:
            return None