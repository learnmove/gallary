# -*- coding: utf-8 -*-
import queue
from ettoday_functions import *

def ettoday(max_mount,que,sem):
    counter = [0]
    
    class single_news(basic_scrapy):#單篇新聞爬蟲
        @exception
        def run_content(self):
            counter[0]+=1
            web = bs(get(self.url))
            obj = self.type,self.url,get_mtext(web)
            que.put(obj)
    class newses(basic_scrapy):#各新聞串爬蟲
        @exception
        def run_content(self):
            web = bs(get(self.url))
            for url,type_ in newslist(web):
                single_news(url,type_).start()
    gen = date_generator()
    while counter[0] < max_mount:
    #for i in range(80):
        url = next(gen)
        newses(url,'').start()#各新聞串爬蟲啟動

if __name__=='__main__':
    que = queue.Queue()
    sem = sm(10)
    ettoday(5000,que,sem)
    time.sleep(10)
    print('done.')
    while not que.empty():
        obj = que.get()
        print(obj[2] or obj[1])
        print()
        input()
    
