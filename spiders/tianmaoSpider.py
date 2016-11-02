# -*- coding: utf-8 -*-
__author__ = 'xwy'

from scrapy.spider import Spider
from items import TianMaoProductItem

from scrapy.selector import Selector
from scrapy import Request
from scrapy import log
from extentions.ParseUtil import xpathUtil

import time
import re
import os

class tianmaoSpider(Spider):
    name = 'tianmaoSpider'
    download_delay = 10
    #name_prefix = 'tianmao_new'
    path = 'D:/tmall/'
    crawl_time_name = time.strftime('%Y-%m-%d %H %M %S', time.localtime(time.time()))
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = str(path) + 'guba_' + str(crawl_time_name) + '.txt'
    spider_begin_time = None
    start_urls = ['https://www.tmall.com/']

    product_list_rule = '//div[@id="J_ItemList"]/div/div'
    product_price_rule = 'div[1]/p[1]/em/text()|div[1]/div[2]/p[1]/text()'
    product_link_rule = 'div[1]/div/h4/a'
    product_shop_rule = 'div[1]/p[3]/a|div[1]/div[3]/p[1]/a'
    product_status_rule = 'div[1]/p[2]/em/text()|div[1]/div[2]/p[3]/span/strong/text()'
    brand_name_rule = 'div[2]/div/span[1]/a/text()'
    product_id_pattern = re.compile('[?&]id=(\d+)&')
    product_skuid_pattern = re.compile('[?&]skuId=(\d+)&')
    user_id_pattern = re.compile('user_id=(\d+)&')

    base_url = 'https://list.tmall.com/search_product.htm'
    main_url = 'https://list.tmall.com/search_product.htm?cat=%s&style=l&sort=p'
    cat_list = ['50024400']
    #cat_list = ['50900004','50025174','50026502']

    def parse(self, response):
        self.spider_begin_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
            start_price = 0.0
            end_price = 10.0
            url_list = []
            while True:
                url = self.main_url + '&start_price=' + str(start_price)
                if end_price:
                    price_range = str(start_price) +  '-' + str(end_price)
                    url += '&end_price=' + str(end_price)
                    url_list.extend([{'url':(url % cat),'price_range':price_range,'cat_id':cat} for cat in self.cat_list])
                    start_price = end_price + 0.01
                else:
                    price_range = str(start_price) + '-'
                    url_list.extend([{'url':(url % cat),'price_range':price_range,'cat_id':cat} for cat in self.cat_list])
                    break
                if start_price < 10:
                    delta = 9.99
                elif 10 <= start_price <45:
                    delta = 4.99
                elif 45 <= start_price < 90:
                    delta = 0.99
                elif 90 <= start_price < 100:
                    delta = 0.49
                elif 100 <= start_price < 130:
                    delta = 1.99
                elif 130 <= start_price < 200:
                    delta = 0.99
                elif 200 <= start_price < 250:
                    delta = 4.99
                elif 250 <= start_price < 290:
                    delta = 1.99
                elif 290 <= start_price < 300:
                    delta = 0.99
                elif 300 <= start_price < 330:
                    delta = 9.99
                elif 330 <= start_price < 350:
                    delta = 4.99
                elif 350 <= start_price < 390:
                    delta = 1.99
                elif 390 <= start_price < 400:
                    delta = 0.99
                elif 400 <= start_price < 430:
                    delta = 9.99
                elif 430 <= start_price < 450:
                    delta = 4.99
                elif 450 <= start_price < 490:
                    delta = 1.99
                elif 490 <= start_price < 500:
                    delta = 0.99
                elif 500 <= start_price < 10000:
                    delta = 49.99
                elif 10000 <= start_price < 20000:
                    delta = 9999.99
                else:
                    delta = None

                if delta:
                    end_price = start_price + delta
                else:
                    end_price = None

            for url in url_list:
                log.msg('爬取链接为：' + url['url'],level=log.INFO)
                yield Request(url=url['url'],meta={'price_range':url['price_range'],'cat-id':url['cat_id'],'is_first_page':True},
                              callback=self.get_product_list,dont_filter=True)
        except Exception,e:
            print 'parse response failed...'
            log.msg('parse response failed',level=log.INFO)

    def get_product_list(self,response):
        try:
            # try block
            sel = Selector(response)
            cat_id = response.meta['cat_id']
            is_first_page = response.meta['is_first_page']
            dont_find_next_page = response.meta.get('dont_find_next_page')

            product_list = sel.xpath(self.product_list_rule)
            totalNum = xpathUtil.get_data(sel.xpath('//p[@class="crumbTitle j_ResultsNumber"]/span/text()').extract(),0)
            totalNum = int(totalNum.strip())
            totalPage = xpathUtil.get_data(sel.xpath('//input[@name="totalPage"]/@value').extract(),0)

            if is_first_page and totalNum > 8400:
                price_range = response.meta['price_range']
                p1,p2 = tuple(price_range.split('-'))
                decimal_num = max(len(p1[p1.index('.')+1:]),len(p2[p2.index('.')+1:]))
                p1,p2 =  float(p1),float(p2)
                if p1 > p2:
                    return
                elif p1 == 0:
                    decimal_num = 2
                    delta = (p2 - p1)/2
                else:
                    delta = (p2 + pow(10,-decimal_num) - p1)/2
                delta = round(delta,4)
                tmp_delta = str(delta)
                decimal_num = max(decimal_num,len(tmp_delta[tmp_delta.index('.')+1:]))
                if p1 == p2 or delta == pow(10,-decimal_num):
                    self.save_product_list(product_list,response.meta['price_range'],cat_id)
                    response.meta['is_next_page'] = False
                    yield Request(url=response.url.replace('sort=p','sort=p&s=84'),
                                  meta=response.meta,
                                  callback=self.save_product_list,
                                  dont_filter=True)
                else:
                    start_price1 ,end_price1 = str(p1),str(p1 + delta - pow(10,-decimal_num))
                    start_price2,end_price2 = str(p1 + delta),str(p2)
                    yield Request(url=self.main_url % cat_id + '&start_price=' + start_price1 + '&end_price=' + end_price1,
                                  meta={'price_range':start_price1 + '-' + end_price1,'cat_id':cat_id,'is_first_page':True},
                                  callback=self.get_product_list,dont_filter=True)
                    yield Request(
                        url=self.main_url % cat_id + '&start_price=' + start_price2 + '&end_price=' + end_price2,
                        meta={'price_range': start_price2 + '-' + end_price2, 'cat_id': cat_id, 'is_first_page': True},
                        callback=self.get_product_list, dont_filter=True)
            else:
                # else block
                print response.meta['price_range'],totalNum,totalPage,response.url
                self.save_product_list(product_list,response.meta['price_range'],cat_id)
                if not dont_find_next_page:
                    next_page = xpathUtil.get_data(sel.xpath('//a[@class="ui-page-s-next"]/@href').extract(),0)
                    if next_page:
                        meta = response.meta.copy()
                        meta['is_first_page']
                        yield Request(url=self.base_url+next_page,meta=meta,callback=self.get_product_list,dont_filter=True)

        except Exception,e:
            print 'get_prodict_list failed...'
            log.msg('get_prodict_list failed',logLevel=log.INFO)

    def save_product_list(self,product_list,price_range,cat_id):
        for product in product_list:
            product_price = xpathUtil.get_data(product.xpath(self.product_price_rule).extract(),0)
            product_link = product.xpath(self.product_link_rule)
            product_title = ' '.join(product_link.xpath('text()').extract())
            product_detail_href = xpathUtil.get_data(product_link.xpath('@href').extract(),0)
            if not product_detail_href:
                product_detail_href = ''
            product_sku_id = re.findall(self.product_skuid_pattern,product_detail_href)
            product_id = re.findall(self.product_id_pattern,product_detail_href)
            product_sku_id = product_sku_id[0] if product_sku_id else None
            product_id = product_id[0] if product_id else None
            product_shop = product.xpath(self.product_shop_rule)
            product_shop_name = xpathUtil.get_data(product_shop.xpath('text()').extract(),0)
            product_shop_href = xpathUtil.get_data(product_shop.xpath('@href').extract(),0)
            product_status = xpathUtil.get_data(product.xpath(self.product_status_rule).extract(),0)
            if cat_id in ['50024400']:
                product_t_and_b = product_title.split(' ',1)
                brand_name = product_t_and_b[0]
            else:
                brand_name = xpathUtil.get_data(product.xpath(self.brand_name_rule).extract(),0)

            item = TianMaoProductItem()
            item['cat_id'] = cat_id
            item['product_price'] = product_price
            item['product_title'] = product_title
            item['product_id'] = product_id
            item['product_sku_id'] = product_sku_id
            item['product_url'] = 'https:' + product_detail_href
            item['product_shop_name'] = str(product_shop_name)
            item['product_shop_url'] = None
            if product_shop_href:
                item['product_shop_url'] = 'https://list.tmall.com/' + str(product_shop_href)
            item['product_status'] = product_status
            item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #item['flag'] =
            item['product_price_range'] = price_range
            item['brand_name'] = brand_name

            with open(self.file_name,'a') as f:
                f.write(item['cat_id'].encode('gbk') + ' ' +
                        item['product_price'].encode('gbk') +  ' ' +
                        item['product_title'].encode('gbk') +  ' ' +
                        item['product_id'].encode('gbk') +  ' ' +
                        item['product_sku_id'].encode('gbk') +  ' ' +
                        item['product_url'].encode('gbk') +  ' ' +
                        item['product_shop_name'].encode('gbk') +  ' ' +
                        item['product_shop_url'].encode('gbk') +  ' ' +
                        item['product_status'].encode('gbk') +  ' ' +
                        item['crawl_time'].encode('gbk') +  ' ' +
                        item['product_price_range'].encode('gbk') +  '\n')

            yield item