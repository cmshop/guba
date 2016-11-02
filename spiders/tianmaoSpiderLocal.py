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

class tianmaoSpiderLocal(Spider):
    name = 'tianmaoSpiderLocal'
    download_delay = 3
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

    test_url = 'https://list.tmall.com/search_product.htm?cat=50024400&sort=s&style=l&s='
    def parse(self, response):
        for i in range(10):
            url_temp = self.test_url + str(84*i)
            yield Request(url=url_temp,callback=self.get_product_list)

    def get_product_list(self,response):
        sel = Selector(response)
        product_list = sel.xpath(self.product_list_rule)
        self.save_product_list(product_list,'none','50024400')

    def save_product_list(self, product_list, price_range, cat_id):
        for product in product_list:
            product_price = xpathUtil.get_data(product.xpath(self.product_price_rule).extract(), 0)
            product_link = product.xpath(self.product_link_rule)
            product_title = ' '.join(product_link.xpath('text()').extract())
            product_detail_href = xpathUtil.get_data(product_link.xpath('@href').extract(), 0)
            if not product_detail_href:
                product_detail_href = ''
            product_sku_id = re.findall(self.product_skuid_pattern, product_detail_href)
            product_id = re.findall(self.product_id_pattern, product_detail_href)
            product_sku_id = product_sku_id[0] if product_sku_id else None
            product_id = product_id[0] if product_id else None
            product_shop = product.xpath(self.product_shop_rule)
            product_shop_name = xpathUtil.get_data(product_shop.xpath('text()').extract(), 0)
            product_shop_href = xpathUtil.get_data(product_shop.xpath('@href').extract(), 0)
            product_status = xpathUtil.get_data(product.xpath(self.product_status_rule).extract(), 0)
            if cat_id in ['50024400']:
                product_t_and_b = product_title.split(' ', 1)
                brand_name = product_t_and_b[0]
            else:
                brand_name = xpathUtil.get_data(product.xpath(self.brand_name_rule).extract(), 0)

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
            item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # item['flag'] =
            item['product_price_range'] = price_range
            item['brand_name'] = brand_name

            with open(self.file_name, 'a') as f:
                f.write(item['cat_id'].encode('gbk') + ' ' +
                        item['product_price'].encode('gbk') + ' ' +
                        item['product_title'].encode('gbk') + ' ' +
                        item['product_id'].encode('gbk') + ' ' +
                        item['product_sku_id'].encode('gbk') + ' ' +
                        item['product_url'].encode('gbk') + ' ' +
                        item['product_shop_name'].encode('gbk') + ' ' +
                        item['product_shop_url'].encode('gbk') + ' ' +
                        item['product_status'].encode('gbk') + ' ' +
                        item['crawl_time'].encode('gbk') + ' ' +
                        item['product_price_range'].encode('gbk') + '\n')

            yield item

