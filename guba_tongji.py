#coding:utf-8
from MyThread import Thread
import threading
import sys,time

file_name = 'gubalist_top500.txt'
with open(file_name,'r') as f:
    res_list = [x.split('\n')[0] for x in f]

name_list = list(set(res_list))

total_names = len(name_list)

def worker(list):
    value = list.pop()
    num = 0
    for item in res_list:
        if item == value:
           num += 1
    print value + ' ' + str(num)
    mutex.acquire()
    with open('guba_tongji_res_top500.txt','a') as f:
        f.write(value + ' ' + str(num) + '\n')
    mutex.release()

def main():
    threads = []
    pool_num = 20
    global mutex
    mutex = threading.Lock()

    for i in range(pool_num):
        t = Thread(worker,name_list)
        threads.append(t)
    for i in range(pool_num):
        threads[i].start()
    for i in range(pool_num):
        threads[i].join()

if __name__ == '__main__':
    main()
    print 'all done'
    time.sleep(5)
    sys.exit()
