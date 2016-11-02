#coding:utf-8

import sys
import importlib
from spiders.gubaSpider import gubaSpider
# scrapy api
from scrapy import signals,log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
import settings


def spider_closing(spider):
    # Activates on spider closed signal
    log.msg('closing reactor',level=log.INFO)
    reactor.stop()

log.start(loglevel=log.DEBUG) # logfile=settings.LOG_FILE,

settings = Settings()

# crawl responsibly
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
crawler = Crawler(settings)

# stop reactor when spider closes
crawler.signals.connect(spider_closing,signal=signals.spider_closed)


path_prefix = 'spiders.'
if len(sys.argv) > 1:
    spider_name = sys.argv[1]
    try:
        custom_spider = importlib.import_module(path_prefix + sys.argv[1])
        spider_class = getattr(custom_spider, spider_name)
        spider = spider_class()
    except Exception,e:
        print 'spider:%s 加载失败 ,error:'%spider_name,e
        log.msg('spider:%s 加载失败 ,error:'%spider_name + str(e),logLevel=log.ERROR)
else:
    print '未提供加载的spider'
    log.msg('未提供加载的spider',logLevel=log.INFO)

crawler.configure()
crawler.crawl(spider) # custom_spider.gubaSpider()
crawler.start()
reactor.run()

