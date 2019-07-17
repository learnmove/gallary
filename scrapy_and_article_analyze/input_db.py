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
    #類別對照表，依照你網站的分類更改，改前先說一聲想怎麼改
    category_dic = {"政治":"政治",
                    "財經":"投資",
                    "論壇":"政治",
                    "國際":"政治",
                    "大陸":"政治",
                    "社會":"生活",
                    "地方":"生活",
                    "新奇":"生活",
                    "生活":"生活",
                    "寵物動物":"生活",
                    "影劇":"娛樂",
                    "體育":"運動",
                    "旅遊":"娛樂",
                    "消費":"娛樂",
                    "名家":"娛樂",
                    "ET來了":"閒聊",
                    "3C家電":"科技",
                    "健康":"生活",
                    "男女":"心情",
                    "公益":"生活",
                    "遊戲":"遊戲",
                    "電影":"娛樂",
                    "時尚":"娛樂",
                    "網搜":"閒聊",
                    "電商":"投資",
                    "親子":"心情",
                    "房產雲":"投資",
                    "ET車雲":"娛樂",
                    "軍武":"政治",
                    "保險":"投資",
                    "法律":"學術",
                    "直銷雲":"投資",
                    "探索":"生活"}
    #類別對照表，依照你網站的分類更改，改前先說一聲想怎麼改
    ######
    
    

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
    ettoday_scrapy.start(100000,que,sem)
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
                sleep(600)
                if que.empty():break
        except:pass
    #關鍵運行串，勿改
    ######

