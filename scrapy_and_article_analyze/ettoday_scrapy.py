# -*- coding: utf-8 -*-
import queue
import time
from random import randint as rd
from ettoday_functions import *
import sqlite3 as sql

@exception
def start(max_mount,que,sem):
    counter = [0]
    class single_news(basic_scrapy):#單篇新聞爬蟲
        @exception
        def run_content(self):
            counter[0]+=1
            web = bs(get(self.url))
            obj = self.type,self.url,get_mtext(web)
            que.put(obj)
            
    @exception
    
    class newses(basic_scrapy):#各新聞串爬蟲
        @exception
        def run(self):
            db = sql.connect('test.db')
            cs = db.cursor()
            web = bs(get(self.url))
            if not web : return
            thr_list=[]
            for url,type_ in newslist(web):
                cs.execute("select * from urls where url = '{}'".format(url))
                result=cs.fetchone()
                if not result:thr_list.append(single_news(url,type_))
                if len(thr_list)>=10:
                    for obj in thr_list:obj.start()
                    for obj in thr_list:obj.join()
                    thr_list=[]
            db.close()
    thr_list=[]
    for url in date_generator():
        if counter[0] > max_mount:break
        thr_list.append(newses(url,''))#各新聞串爬蟲啟動
        if len(thr_list)>=10:
            for obj in thr_list:obj.start()
            for obj in thr_list:obj.join()
            thr_list=[]

    print('finish.')

if __name__=='__main__':
    que = queue.Queue()
    sem = sm(10)
    start(500,que,sem)
    time.sleep(10)
    print('done.')
    while not que.empty():
        input()
        print(que.qsize())
        obj = que.get()
        print(obj[2] or obj[1])
        print()
        
    
