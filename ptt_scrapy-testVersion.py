# -*- coding: utf-8 -*-

import queue
import re
import requests
from bs4 import BeautifulSoup as bs
from random import randint as rd
from threading import Thread as thr
from threading import Semaphore as sm
from time import sleep

max_num_of_pieces = 100
que = queue.Queue()
sem = sm(30)
boardSM = sm(10)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
mainurl = 'https://www.ptt.cc'
url = 'https://www.ptt.cc/bbs/index.html'
counter=[0]#計數器，設為list裡面有個值，這樣不管在第幾層的function都可以直接加而不用宣告global或nonlocal

#預防18禁限制，這邊先一次解決掉
#用session()覆蓋掉requests這命名，這樣後面用的requests就都會有session了
#payload裡設定的關係，結果會直接導向ptt首頁
requests = requests.Session()
payload = {
        'from':'/bbs/index.html',
        'yes':'yes'
        }
soup = bs(requests.post('https://www.ptt.cc/ask/over18', headers = headers,data = payload).text,'html.parser')

#抓文章內文的執行緒，導入參數為網址跟討論版分類
class article(thr):
    def __init__(self,url,type_):
        thr.__init__(self,name=url)#將執行緒名稱設為導入之url，當報錯時可以方便去該網址查看究竟
        self.url = url
        self.type = type_
    def run(self):
        sem.acquire()#獲取旗標semephore，如果旗標數量不夠，執行緒會暫停直到拿到旗標
        counter[0]+=1#執行緒開始時計數
        page = bs(requests.get(self.url, headers = headers).text,'html.parser')
        Mtext = page.find('div',id = 'main-content')#如果文章不存在Mtext會是None，再.text會報錯，所以設if檢測
        if Mtext and Mtext.text and '發信站' in Mtext.text:#但Mtext.text之後也有可能是None，所以再接and檢測一次
            #發信站是正常發文之下內文的結束點，如下:
            #--
            #※ 發信站: 批踢踢實業坊(ptt.cc), 來自: 27.52.126.188 (臺灣)
            #如果沒有發信站三字代表文章被過度編輯，該文不適用
            txt = re.split('\n+',Mtext.text)#re內的split切片功能，很強大，可以把匹配到的字元當成切割符做split
            for i,v in enumerate(txt):
                if '發信站' in v:break#內文截取，排除後面的推文，break時i表示文章結束的下兩行，所以[1:i-1]
            txt = ' '.join(txt[1:i-1])#放進queue時內文需是一個完整的string而非切片後的list
            que.put((self.type,self.url,txt))
            
        sem.release()#旗標釋放
        
#此為各討論版塊的執行緒，負責找到文章連結並發配給article執行緒，執行翻頁，導入參數為網址跟討論版分類
class board(thr):
    def __init__(self,url,type_):
        thr.__init__(self,name=url)
        self.url = url
        self.type = type_
    def run(self):
        while 1:#因為有設中斷條件了，所以直接無限迴圈
            if counter[0] > max_num_of_pieces:break#中斷條件為counter計數，要是大於導入的變數則break
            soup = bs(requests.get(self.url, headers = headers).text,'html.parser')
            for arti in soup.find_all('div',class_ = 'r-ent'):
                if counter[0] > max_num_of_pieces:break#兩層迴圈都要設中斷條件
                try:#有時會碰到None的問題，所以設個try
                    artic = arti.find('div',class_ = 'title')
                    title = artic.text
                    if re.search('公告|問卷|刪除',title):continue#如果文章屬於公告或者問卷或者已經被刪除則跳過
                    artiLink = artic.find('a').get('href')
                except:continue
                link = mainurl + artiLink
                article(link,self.type).start()#發配給article執行緒，直接一行寫掉直接執行
                sleep(0.1+rd(0,100)/1000)#每發配一篇文章後暫停0.1~0.2秒
            self.url = mainurl + soup.find('a',string = '‹ 上頁')['href']#下一頁

#此為主執行緒，尋找ptt上各大討論版塊網址並發配給board執行緒
for board_ in soup.find_all('div',class_ = 'b-ent'):
    type_ = board_.find('div',class_ = 'board-class').text
    link = mainurl+board_.find('a')['href']
    board(link,type_).start()#發配給board執行緒，直接一行寫掉直接執行
