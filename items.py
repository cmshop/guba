# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GubaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    num = scrapy.Field()
    stk_name = scrapy.Field()
    stk_code = scrapy.Field()
    crawl_time = scrapy.Field()

class GubaListItem(scrapy.Item):
    name = scrapy.Field()
    #num = scrapy.Field()
class XueqiuItem(scrapy.Item):
    comm_id = scrapy.Field()
    item = scrapy.Field()
    item_name = scrapy.Field()
    timeBefore = scrapy.Field()
    text = scrapy.Field()
    reply_count = scrapy.Field()
    user_id = scrapy.Field()
    crawl_time = scrapy.Field()
    retweet_count = scrapy.Field()
    fav_count = scrapy.Field()
    reward_count = scrapy.Field()
    retweeted_status = scrapy.Field()

class TianMaoProductItem(scrapy.Item):
    cat_name = scrapy.Field()
    cat_id = scrapy.Field()
    product_title = scrapy.Field()
    product_id = scrapy.Field()
    product_sku_id = scrapy.Field()
    product_url = scrapy.Field()
    product_price_range = scrapy.Field()
    product_price = scrapy.Field()
    product_shop_name = scrapy.Field()
    product_shop_url = scrapy.Field()
    product_status = scrapy.Field()
    crawl_time = scrapy.Field()
    flag = scrapy.Field()
    brand_name = scrapy.Field()

class DuTiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cat_fir = scrapy.Field()
    cat_sec = scrapy.Field()
    title = scrapy.Field()
    attention_num = scrapy.Field()
    article_num = scrapy.Field()
    flag = scrapy.Field()

class KalLaItem(scrapy.Item):
    cat_id = scrapy.Field()
    cat_name = scrapy.Field()
    product_id =scrapy.Field()
    product_title = scrapy.Field()
    product_price_origion = scrapy.Field()
    product_price_current = scrapy.Field()
    product_comment_num = scrapy.Field()
    product_selfflag = scrapy.Field()
    flag = scrapy.Field()
    crawler_time = scrapy.Field()

class YanXuanItem(scrapy.Item):
    cat_id = scrapy.Field()
    cat_name = scrapy.Field()
    product_id =scrapy.Field()
    product_title = scrapy.Field()
    product_price_current = scrapy.Field()
    product_comment_num = scrapy.Field()
    flag = scrapy.Field()
    crawler_time = scrapy.Field()

class AutoHomeItem(scrapy.Item):
    cat_id = scrapy.Field()
    cat_name = scrapy.Field()
    address = scrapy.Field()
    product_price_origion = scrapy.Field()
    product_price_current = scrapy.Field()
    product_title = scrapy.Field()
    sales = scrapy.Field()
    flag = scrapy.Field()
    crawler_time = scrapy.Field()