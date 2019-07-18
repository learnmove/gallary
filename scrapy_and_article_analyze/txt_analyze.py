# -*- coding: utf-8 -*-
import sqlite3 as sql
import math
import random
import koten_analyze
from db_functions import str_to_dic

db = sql.connect('test.db')
cursor = db.cursor()

#讀取關鍵字列表
cursor.execute("select * from key_words where length(name)>1 order by val desc")
key_words = {res[0]:{'val':res[1],'types':str_to_dic(res[2])} for res in cursor.fetchall()}
for key in key_words:
    type_dic = key_words[key]['types']
    type_sum = sum(type_dic.values())
    for type_ in type_dic:
        type_dic[type_]=type_dic[type_]/type_sum

#讀取文章總數
cursor.execute("select val from variable where name = 'total_amount'")
total_amount = cursor.fetchone()[0]

#讀取url列表並打亂
cursor.execute("select * from urls")
result = cursor.fetchall()
type_dic = {i[0]:[] for i in result}
for i in result : type_dic[i[0]].append(i[1])
for key in type_dic : random.shuffle(type_dic[key])
    
def txt_class(txt):
    def log(x):
        return math.log(x,10)
    def importance(word):
        try:return log(total_amount/key_words[word]['val'])
        except KeyError:return 1
    result = {key:val for dic in koten_analyze.txt_analyze(txt)[1].values() for key,val in dic.items() if len(key)>1}
    total_words_amount = sum(result.values())
    txt_type = {key:0 for key in type_dic}
    for key,val in result.items():
        newval=val/total_words_amount*importance(key)
        result[key]=newval
        if key in key_words:
            key_types = key_words[key]['types']
            for i,v in key_types.items():
                txt_type[i]+=v*newval
    return sorted(txt_type,key=lambda x:txt_type[x],reverse=True)[0]

if __name__=='__main__':

    txt='''
網路流傳泡麵吃法百百種，像是之前流行的加起士、牛奶或是布丁，將簡單的泡麵再升級，或是創造出跟原本完全不同口味的泡麵，現在網路上又出現一種新吃法，沒想到這新吃法的背後居然有個塞滿洋蔥的故事讓網友哭紅了眼。

有位網友在ptt上PO文分享，「心目中的泡麵配料之王」此文一出竟引來大量網友留言，其中有篇回文更是讓鄉民們大喊有洋蔥。

這篇寫到黃金豆腐才是最完美的配料，一位即將論及婚嫁的男友外遇了，分手當晚突然把所有東西搬回家，還抱著爸媽崩潰大哭，爸媽錯愕但也沒多說多問，只端著一碗熱熱的泡麵上面還加了一塊黃金豆腐，旁邊紙條寫著“你一直都是我們最棒的女兒”，突然間就頓悟，失戀沒什麼再找就好。

貼文曝光後，引發許多網友共鳴，大家紛紛留言，「恭喜妳～有愛妳的爸媽，還遠離了渣男～」、「是中華的黃金豆腐嗎？我也要買來吃」、「失戀沒什麼，附上單身族的我平時也愛泡麵加黃金豆腐」、「好溫暖的故事 希望也能成為像你爸媽這樣的人」、「有媽媽最好～不說了今天晚上就決定是泡麵＋黃金豆腐」、「這篇配的不是豆腐是洋蔥QQ」、「推爸媽 也推中華黃金豆腐真的好吃 渣男滾」。

'''
    print(txt_class(txt))

