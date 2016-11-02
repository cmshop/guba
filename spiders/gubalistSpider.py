#coding:utf-8
from scrapy.spider import Spider
from scrapy.http import Request
#from guba.items import GubaItem
from items import GubaItem,GubaListItem

class gubalistSpider(Spider):
    '''
    股吧首页全部下 热门回帖的 前N页的帖子对应的吧名 最后在汇总 以统计该吧一段时期的活跃度

    '''
    name = 'gubalistSpider'
    allowed_domain = 'eastmoney.com'
    start_urls = ['http://guba.eastmoney.com/default_1.html']

    name_rule = '//span[@class="sub"]/a[@class="balink"]/'
    span_rule = '//li/span[@class="sub"]'

    def parse(self, response):
        #self.get_content(response)

        for i in range(1,100):
            base_url = self.start_urls[0].split('_')[0]
            next_url = base_url + '_' + str(i) + '.html'
            yield Request(url=next_url,callback=self.get_content)

    def get_content(self,response):
        if response:
            try:
                spans = response.xpath(self.span_rule)
                if spans:
                    for span in spans:
                        temp = span.xpath('./em[@class="settop"]')
                        if not temp:
                            name = self.get_data(span.xpath('./a/text()').extract(),0)
                            if name:
                                item = GubaListItem()
                                item['name'] = name
                                with open('D:/gubalist_top100.txt','a') as f:
                                    f.write(item['name'].encode('gbk') + '\n')
                                #yield item
                else:
                    print 'span got none'
            except Exception,e:
                print 'get-cotent error ',e
        else:
            print 'response none'

    def get_data(self,list,index):
        if list and index < len(list):
            return list[index]
        else:
            return None