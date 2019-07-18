# -*- coding: utf-8 -*-
import re
from math import log
from basic_tools import *
level=8

@exception
def start(txt):
    return cleaner(*txt_analyze(txt))

class phrase:
    def __init__(self,length):
        self.body = ''
        self.length = length
    @exception
    def put(self,val):
        if type(val)!=str:return
        self.body+=val
        if len(self.body)>self.length:
            self.body = self.body[1:]
        if len(self.body)==self.length:
            return self.body

class counter:
    def __init__(self):
        self.dic={i+1:{} for i in range(level+1)}
        self.length = 0
    @exception
    def word_dissociate(self,txt):
        phrases = [phrase(i+1) for i in range(level+1)]
        txt = re.sub('[的啊哈啦]+','',txt)
        for s in txt:
            self.length += 1
            for e in phrases:
                word = e.put(s)
                if word:
                    if word in self.dic[e.length]:
                        self.dic[e.length][word]+=1
                    else:self.dic[e.length][word]=1
                    
@exception
def txt_analyze(txt):
    count_dic = counter()
    for sentence in re.split('[\Wa-zA-Z0-9_]+',txt):
        count_dic.word_dissociate(sentence)
    dic = count_dic.dic
    del_list = set()
    #delcount = 0
    for num in range(level+1,0,-1):
        if num-1 in dic:
            pre_del_list = set()
            for word,val in dic[num].items():
                for nextword in [word[1:],word[:-1]]:
                    if nextword in dic[num-1] and abs(dic[num-1][nextword]-val)/val<=0.01:
                        pre_del_list.add(nextword)
                        #del because it's a child
            for word in del_list:
                del dic[num][word]
                #delcount+=1
            del_list = pre_del_list
    return count_dic.length,dic

@exception
def cleaner(length,dic):
    var_clean = int(log(length,1.59))-11
    var_output = int(log(length,11.22))-1 or 1

    for num in range(level+1,0,-1):
        del_list = set()
        for word,val in dic[num].items():
            if val<=var_clean:
                del_list.add(word)
                continue
            
        for word in del_list:
            del dic[num][word]

    return {j:var_output for i in dic.values() for j in i.keys()}

if __name__=='__main__':

    txt='''
國民黨總統初選參選人郭台銘主張，當選總統後，將徵收富人稅。他11日重申，「富人多繳稅，全民都受惠」，社會上有錢的人，可能是比較有能力的人，但更可能只是比較幸運的人，不論是何者，都不應該獨善其身，而是要善盡社會責任，幫助更多有需要的人，才能打造公平正義、富而好禮的國家社會。

郭台銘在臉書提到，過去幾十年，他的事業賺了很多錢，繳了超過四千億的稅，納稅之餘，自己也再捐一千多億元作為慈善公益，都是出於一顆取之於社會，用之於社會的心，出來選總統是因為想要做更多，想集合社會上有能力的人，一起幫助更多的人過更好的日子。

郭台銘指出，我們的社會並不反對富人存在，但希望富人能多做好事，不要為富不仁，打造為富有仁、公平正義的和諧社會，是他想要的中華民國社會，而主張開徵富人稅，不是和誰有仇，而是看到少數人有能力做更多卻不做，有更多人有需要但等不到，實在不是一個「有仁」的社會。

郭台銘更以禮運大同篇來表達他徵富人稅的理念，「人不獨親其親，不獨子其子；使老有所終，壯有所用，幼有所長，矜、寡、孤、獨、廢疾者，皆有所養」，富人多繳稅，繳比現在更多的稅，才足以讓陷於「悶經濟」的國家持續提升，讓苦於「窮忙」的全民都能受惠。
'''
    dic = start(txt)
