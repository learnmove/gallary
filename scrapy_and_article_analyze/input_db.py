# -*- coding: utf-8 -*-

######
#關鍵模組，勿改
from db_functions import *
#關鍵模組，勿改
######

######
#請改成你要用的爬蟲檔案

import ettoday_scrapy

#請改成你要用的爬蟲檔案
######

if __name__=='__main__':

    ######
    #關鍵運行串，勿改
    db = sql.connect('test.db')
    cursor = db.cursor()
    que=queue.Queue()
    sem = sm(10)
    #關鍵運行串，勿改
    ######

    #####
    #請改成你爬蟲用的function，第一個參數如果爬的是小說就改1萬
    thr(target=ettoday_scrapy.start,args=(100000,que,sem)).start()
    #請改成你爬蟲用的function，第一個參數如果爬的是小說就改1萬
    #####

    ######
    #關鍵運行串，勿改
    print('go')
    while 1:
        try:
            if not que.empty():
                type,url,txt = que.get()
                print(type,url)
                
                cursor.execute("select * from urls where url = '{}'".format(url))
                result = cursor.fetchone()
                if len(re.sub('[\Wa-zA-Z0-9_]+','',txt))<200 or result:
                    print('drop out.'+('find url.' if result else ''))
                    continue
                analyze_and_input(type,url,txt)
            else:
                print('waiting.')
                sleep(30)
                if que.empty():break
        except:pass
    #關鍵運行串，勿改
    ######

