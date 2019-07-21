# -*- coding: utf-8 -*-
import re
import copy
import time
import queue
import sqlite3 as sql
from threading import Semaphore as sm
from time import sleep
if __name__=='__main__':
    import os,sys
    sys.path.append('\\'.join(os.getcwd().split('\\')[:-1]))
from tools.basic import exception
import tools.koten_analyze as analyze

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
    return str(dic)
@exception
def str_to_dic(string):
    exec('dic='+string,locals())
    return locals()['dic']
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
