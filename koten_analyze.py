# -*- coding: utf-8 -*-
import re
level=9

class phrase:
    def __init__(self,lenth):
        self.body = ''
        self.lenth = lenth
    def put(self,val):
        if type(val)!=str:return
        self.body+=val
        if len(self.body)>self.lenth:
            self.body = self.body[1:]
        if len(self.body)==self.lenth:
            return self.body

class counter:
    def __init__(self):
        self.dic={i+1:{} for i in range(level+1)}
    def word_dissociate(self,txt):
        phrases = [phrase(i+1) for i in range(level+1)]
        for s in txt:
            if s in '的啊哈啦':
                phrases = [phrase(i+1) for i in range(level+1)]
                continue
            for e in phrases:
                word = e.put(s)
                if word:
                    if word in self.dic[e.lenth]:
                        self.dic[e.lenth][word]+=1
                    else:self.dic[e.lenth][word]=1

def novel_analyse(txt):
    count_dic = counter()
    for sentence in re.split('\W+',txt):
        count_dic.word_dissociate(sentence)
    #count by each phrases lenth
    dic = count_dic.dic
    del_list = set()
    #delcount = 0
    for num in range(level+1,0,-1):
        pre_del_list = set()
        for word,val in dic[num].items():
            if val<=10:
                del_list.add(word)
                #del word because val=1
                continue
            if num-1 in dic:
                for nextword in [word[1:],word[:-1]]:
                    # dic[num-1][nextword]==val
                    if nextword in dic[num-1] and \
                    abs(dic[num-1][nextword]-val)/val<=0.05:
                        pre_del_list.add(nextword)
                        #del because it's a child
        for word in del_list:
            del dic[num][word]
            #delcount+=1
        del_list = pre_del_list
    #print('delcount :',delcount)
    return dic
                
def txt_analyse(txt):
    count_dic = counter()
    for sentence in re.split('\W+',txt):
        count_dic.word_dissociate(sentence)
    #count by each phrases lenth
    dic = count_dic.dic
    del_list = set()
    #delcount = 0
    for num in range(level+1,0,-1):
        pre_del_list = set()
        for word,val in dic[num].items():
            if val==1:
                del_list.add(word)
                #del word because val=1
                continue
            if num-1 in dic:
                for nextword in [word[1:],word[:-1]]:
                    if nextword in dic[num-1] and dic[num-1][nextword]==val:
                        pre_del_list.add(nextword)
                        #del because it's a child
        for word in del_list:
            del dic[num][word]
            #delcount+=1
        del_list = pre_del_list
    #print('delcount :',delcount)
    return dic



with open('fate-hunter.txt','r',newline='') as file:
    txt=file.read()
    dic = novel_analyse(txt)
