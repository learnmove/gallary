# -*- coding: utf-8 -*-
import os
import csv
import requests
from time import sleep
from random import randint as rd
from bs4 import BeautifulSoup as bs
from threading import Thread as thr
from threading import Semaphore as sm

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
mainurl='https://www.ptt.cc'
url = 'https://www.ptt.cc/bbs/Beauty/index.html'

soup = bs(requests.get(url, headers=headers).text,'html.parser')

link_old={}
pagecount=0
articleSM = sm(10)
imgSM = sm(30)


class imageDL(thr):
    def __init__(self,url,name,semaphore):
        thr.__init__(self)
        self.url = url
        self.name = name
        self.sm = semaphore
        
    def run(self):
        self.sm.acquire()
        
        try:
            jpgQ = requests.get(self.url, headers=headers)
            with open('img\\' + self.name , 'wb' , ) as jpgW :
                for line in jpgQ : jpgW.write(line)
                
        except Exception as exp:
            
            with open('error.txt','a',newline='') as txt:
                txt.write(self.name+'\r\n')
                txt.write(self.url+'\r\n')
                txt.write('- '*5+'\r\n')
                txt.write(str(exp)+'\r\n')
                txt.write('='*30+'\r\n')
                
        self.sm.release()
        
class article(thr):
    def __init__(self,url,title,semaphore):
        thr.__init__(self)
        self.url = url
        self.title = title
        self.sm = semaphore
        print(title)
    def run(self):
        self.sm.acquire()
        try:
            img = 'null'
            page = bs(requests.get(self.url, headers=headers).text,'html.parser')
            jpglist = [a['href'] for a in page.find_all('a',rel='nofollow') if 'imgur' in a.text]
            index = 0
            for img in jpglist:
                deputy = '.jpg'
                if 'gif' in img : deputy = '.gif'
                elif 'jpeg' in img : deputy = '.jpeg'
                elif 'png' in img : deputy = '.png'
                elif 'jpg' not in img : img,deputy = self.imgur(img)
                name = self.title + str(index).zfill(2) + deputy
                t = imageDL(img,name,imgSM)
                t.__name__ = name
                t.start()
                index += 1
        except Exception as exp:
            with open('error.txt','a',newline='') as txt:
                txt.write(self.title+'\r\n')
                txt.write(self.url+'\r\n')
                txt.write(img+'\r\n')
                txt.write('- '*5+'\r\n')
                txt.write(str(exp)+'\r\n')
                txt.write('='*30+'\r\n')
        self.sm.release()
        
    def imgur(self,url):
        page = bs(requests.get(url, headers=headers).text,'html.parser')
        link = page.find('link',rel='image_src').get('href')
        deputy = link.split('.')[-1]
        return link,'.'+deputy

try:
    with open('img\\test','w'):pass
    os.remove('img\\test')
except:os.mkdir('img')

try:
    with open('Beauty.csv','r',newline='',encoding='utf-8-sig') as beauty:
        for i in list(csv.reader(beauty)):
            link_old[i[0]]=i[1]
except Exception as exp:print(exp)

while pagecount < 100:
    
    link_save = {}
    _next = mainurl + soup.find(class_ = 'btn-group-paging').find_all('a')[1]['href']
    
    for obj in soup.find_all('div',class_='r-ent'):
        try:
            artiA = obj.find('div',class_='title').find('a')
            title = artiA.text
        except:continue
        link = mainurl+artiA.get('href')
        for s in r'\/?:*"<>|':
            title = title.replace(s,'')
        if not '正妹' in title or title in link_old:continue
        else:
            link_save[title]=link
            t = article(link,title,articleSM)
            t.__name__ = title
            t.start()
            sleep(0.1+rd(0,100)/1000)

    soup=bs(requests.get(_next,headers=headers).text,'html.parser')
    
    if link_save :
        pagecount += 1
        with open('Beauty.csv','a',newline='',encoding='utf-8-sig') as li:
            csv.writer(li).writerows(list(link_save.items()))
            
    print('page',pagecount)
