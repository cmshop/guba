#coding:utf-8
import re
import time


class TimeFormat(object):
    def __init__(self,time_before,crawl_time=''):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if crawl_time == '':
            self.crawl_time = self.now
        else:
            self.crawl_time = crawl_time
        self.pre_time = time_before
    def conver2Format(self,):

        if re.search(re.compile(u'\d+分钟前'),self.pre_time):
            delta = int(re.findall(re.compile(u'(\d+)分钟前'),self.pre_time)[0])
            pro_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.crawl_time - delta*60))
            print pro_time
            return pro_time
        elif re.search(re.compile(u'今天 \d{2}:\d{2}'),self.pre_time):
            time_day = time.strftime('%Y-%m-%d', time.localtime(self.crawl_time))
            pro_time = time_day + ' ' + re.findall(re.compile(u'今天 (\d{2}:\d{2})'),self.pre_time)[0] + ':00'
            print pro_time
            return pro_time
        elif re.search(re.compile('^\d{2}-\d{2} \d{2}:\d{2}'),self.pre_time):
            time_year = time.strftime('%Y', time.localtime(self.crawl_time))
            pro_time = time_year + '-' + self.pre_time + ':00'
            print pro_time
            return pro_time
        elif re.search(re.compile('^(\d{4}-\d{2}-\d{2} \d{2}:\d{2})'),self.pre_time):
            print self.pre_time
            return self.pre_time
        else:
            print 'no formating...'
            return None

if __name__ == '__main__':
    t = TimeFormat(u'6分钟前',time.time())
    t.conver2Format()

    t1 = TimeFormat(u'今天 08:32',time.time())
    t1.conver2Format()

    t2 = TimeFormat('08-22 23:53',time.time())
    t2.conver2Format()

    t3 = TimeFormat('2015-09-22 09:09:00')
    t3.conver2Format()