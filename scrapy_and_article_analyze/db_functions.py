# -*- coding: utf-8 -*-
from basic_tools import *
import re
import copy
import time
import queue
import sqlite3 as sql
import koten_analyze as analyze
from threading import Semaphore as sm
from time import sleep
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

db = sql.connect('test.db')
cursor = db.cursor()
    
@exception
def analyze_and_input(type,url,txt):
    type = category_dic[type]
    result = analyze.start(txt)
    if not result:
        print('result empty.')
        return
    
    val = set(result.values()).pop()
    type_dic={type:val}
    
    for key in result:
        keyword_plus(key,val,type_dic)
        
    cursor.execute("insert into {0} values('{1}','{2}')".format('urls',type,url))
    total_amount = db_get('variable','total_amount')[0]
    cursor.execute("update {0} set val={2} where name='{1}'".format('variable','total_amount',total_amount+val))
    db.commit()
@exception
def keyword_plus(key,val,type_dic):
    check = db_get('key_words',key)
    if check:
        pval,pdic = check
        newval=pval+val
        dic = dic_combine(type_dic,str_to_dic(pdic))
        keyword_update('key_words',key,newval,dic)
    else:keyword_insert('key_words',key,val,type_dic)
    
@exception
def dic_to_str(dic):
    s = re.sub("[\'\{\} ]+",'',str(dic))
    return s
@exception
def str_to_dic(string):
    dic={}
    for item in string.split(','):
        key,val = item.split(':')
        dic[key] = int(val)
    return dic
@exception
def db_get(table,keyword):
    cursor.execute("select * from {} where name = '{}'".format(table,keyword))
    result = cursor.fetchone()
    if result:return result[1:]
@exception
def keyword_update(table,keyword,val,dic):
    cursor.execute("update {0} set val={2} ,types='{3}' where name='{1}'".format(table,keyword,val,dic_to_str(dic)))
@exception
def keyword_insert(table,keyword,val,dic):
    cursor.execute("insert into {0} values('{1}',{2},'{3}')".format(table,keyword,val,dic_to_str(dic)))
@exception
def dic_combine(dic1,dic2):#from 2 to 1
    dic=copy.copy(dic1)
    for i,v in dic2.items():
        if i in dic:dic[i]+=v
        else:dic[i]=v
    return dic
