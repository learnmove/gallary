# -*- coding: utf-8 -*-
import queue
from Mobile01_functions import *

def Mobile01(max_mount,que,sem):
    counter = [0]
    
    class board(basic_scrapy):#討論板爬蟲
        @exception
        def run_content(self):
            while self.url:
                web = bs(get(self.url))
                for obj in findall(web,'td',class_="subject"):
                    url = get_url(obj)
                    discussion(url , self.type).start()#討論串爬蟲啟動
                self.url = get_nextpage(web)
                
    class discussion(basic_scrapy):#討論串爬蟲
        @exception
        def run_content(self):
            while self.url and counter[0] < max_mount:
                counter[0] += 1
                soup = bs(get(self.url))
                for i in findall(soup,'div',class_="single-post-content"):
                    mtext = get_mtext(i)
                    if mtext:que.put((self.type,self.url,mtext))
                self.url = get_nextpage(soup)

    soup = bs(get('https://www.mobile01.com/forum.php'))
    for i in findall(soup,'td'):
        if is_type(i):
            type_ = i.text
            url = get_url(i)
            board(url,type_).start()
        else:
            for j in i.find_all('li'):
                url = get_url(j)
                if not url:continue
                board(url,type_).start()#討論板爬蟲啟動

if __name__=='__main__':
    que = queue.Queue()
    sem = sm(10)
    Mobile01(100,que,sem)
