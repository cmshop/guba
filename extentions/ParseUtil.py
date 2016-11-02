# -*- coding: utf8 -*-
__author__ = 'huangzhenfeng'

from scrapy.selector import Selector
import urllib2
#from crawler import extsettings
import re
import time


class xpathUtil():

    def __init__(self):
        pass


    @staticmethod
    def get_data(data, position):
        if data and len(data) > position:
            return data[position]
        else:
            return None

    '''
    @staticmethod
    def get_rule_list(data, rule):
        if data:
            return Selector(data).xpath(rule).extract()
        else:
            return None

    @staticmethod
    def get_rule_text_list(data, rule):
        if data:
            return Selector(text=data).xpath(rule).extract()
        else:
            return None


    @staticmethod
    def is_exist(data, field_name):
        try:
            data = data[field_name]
        except Exception, e:
            data = None
        return data

    @staticmethod
    def auto_xpath(xpth, rule, position):
        try:
            if xpth:
                site = xpth.xpath(rule).extract()
                if site and len(site) > position:
                    return site[position]
                else:
                    return None
            else:
                return None

        except Exception, e:
            return None

    @staticmethod
    def auto_xpath_text(data, rule, position):
        try:
            if data:
                site = Selector(text=data).xpath(rule).extract()
                if site and len(site) > position:
                    return site[position]
                else:
                    return None
            else:
                return None

        except Exception, e:
            return None

    def auto(self, lists, dicts, item):
        for em in lists[::2]:
            if dicts. has_key(em.encode('utf-8')):
                key = dicts[em.encode('utf-8')]
                val = lists[lists.index(em) + 1]
                item[key] = val
        return item

    @staticmethod
    def get_keyword_rivals():
        local_keyword_url = 'http://' + extsettings.OPINION_KEYWORD_HOST + \
                     ':' + str(extsettings.OPINION_KEYWORD_PORT) + extsettings.OPINION_KEYWORD_URL
        try:
            html = urllib2.urlopen(url=local_keyword_url, timeout=5)
            code_list = html.read()

            code_array = str(code_list).replace('[', '').replace(']', '').replace('"', '').split(',')

            return code_array
        except Exception, e:
            print e
            return None

    @staticmethod
    def compare_dates(s_date, base_date=None):
        """
        return True if s_date > base_date else return False

        s_date: 2015-10-10 2015.1.1 2015/1/1 2015年10月1日
        base_date: YYYYMMDD 20131112
        """
        if not s_date:
            return False
        s_date = s_date.replace('年', '-').replace('月', '-')
        date_pattern = re.compile(r'([12]\d{3})[.\-/](\d{1,2})[.\-/](\d{1,2})')
        mg = re.findall(date_pattern, s_date)
        if mg:
            y, m, d = mg[0]
            if len(m)==1:
                m = '0'+m
            if len(d)==1:
                d = '0'+d
            s_date = y + m + d
            if base_date is None:
                now = time.strftime("%Y%m%d", time.localtime(time.time()))
                return s_date > now
            else:
                return s_date > base_date
        else:
            return False



    '''