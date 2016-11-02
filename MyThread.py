#coding:utf-8
# 封装的多线程类
import threading

class Thread(threading.Thread):
    def __init__(self,func,args,name='my_thread'):
        threading.Thread.__init__(self)
        self.func = func
        self.list = args
        self.name = name
    def run(self):
        while len(self.list) > 0:
            #apply(self.func,self.list)
            self.func(self.list)
