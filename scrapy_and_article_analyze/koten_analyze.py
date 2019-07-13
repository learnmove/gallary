# -*- coding: utf-8 -*-
import re
from math import log
level=9

def start(txt):
    class phrase:
        def __init__(self,length):
            self.body = ''
            self.length = length
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
        def word_dissociate(self,txt):
            phrases = [phrase(i+1) for i in range(level+1)]
            txt = re.sub('[的啊哈啦]+','',txt)
            for s in txt:
                for e in phrases:
                    self.length += 1
                    word = e.put(s)
                    if word:
                        if word in self.dic[e.length]:
                            self.dic[e.length][word]+=1
                        else:self.dic[e.length][word]=1

    def txt_analyse(txt):
        count_dic = counter()
        for sentence in re.split('[\Wa-zA-Z0-9]+',txt):
            count_dic.word_dissociate(sentence)
        return count_dic.length,count_dic.dic

    def cleaner(length,dic):
        var_clean = int(log(length,1.62))-8 or 1
        var_output = int(log(length,7.2))-1 or 1
        
        #count by each phrases length
        del_list = set()
        #delcount = 0
        for num in range(level+1,0,-1):
            pre_del_list = set()
            for word,val in dic[num].items():
                if val<=var_clean:
                    del_list.add(word)
                    #del word because val=1
                    continue
                if num-1 in dic:
                    for nextword in [word[1:],word[:-1]]:
                        # dic[num-1][nextword]==val
                        if nextword in dic[num-1] and abs(dic[num-1][nextword]-val)/val<=0.05:
                            pre_del_list.add(nextword)
                            #del because it's a child
            for word in del_list:
                del dic[num][word]
                #delcount+=1
            del_list = pre_del_list
        #print('delcount :',delcount)
        return {j:var_output for i in dic.values() for j in i.keys()}
    return cleaner(*txt_analyse(txt))


if __name__=='__main__':
    with open('fate-hunter.txt','r',newline='') as file:
        txt=file.read()
        dic = start(txt)
