# -*- coding: utf-8 -*-
import re
from net_tools import *

mainurl = 'https://www.ettoday.net/'

@exception
def find_date(soup_obj):
    return find(soup_obj,'span',class_='date').text.split(' ')[0]

@exception
def newslist(soup_obj):
    result = findall(soup_obj,'h3')
    first = True
    if not result:return
    for obj in result:
        
        #篩選條件:h3物件，裡面要有一個em物件，class是"tag c_news"
        type_ = find(obj,'em', class_="tag c_news")
        if type_:type_ = type_.text or "新聞"
        else:continue
        
        date = find_date(obj)
        if first: #先抓到當日日期，以第一個決定
            current_date = date
            first = False
        elif date != current_date : break #如果非當日日期則跳掉

        yield get_url(obj),type_

@exception
def get_url(soup_obj):#->str
    return mainurl + find(soup_obj,'a')['href']

@exception
def get_mtext(soup_obj):#->str
    result = ''
    for line in findall(soup_obj,'p'):
        txt = line.text
        if line.get('class') or re.search('[►▲▼※]+|today',txt):
            continue
        if re.search('^延伸|【.{2}新聞】|其他.+新聞|更多',txt):
            break
        for i in txt.split('\n'):
            if re.search('^記者|報導|^文|^圖',i):
                continue
            result += i + '\r\n'
    if not result:raise Exception('No mtext. as following as: ' + soup_obj.text)
    return result

@exception
def date_generator():
    now = time.time()
    newslist_url = mainurl + 'news/news-list-'
    while now > 1317657600:#這串數字代表為2011-10-4，為ettoday最早的新聞開始
        date = time.strftime("%Y-%m-%d-", time.localtime(now))
        daily_url = newslist_url + date
        for i in range(1,41):
            yield daily_url + str(i) + '.htm' #輸出當日1~40所有分類的網址
        now -= 86400 #回推一天
'''
if __name__ == '__main__':
    for i in date_generator():
        print(i)
    input()
'''
