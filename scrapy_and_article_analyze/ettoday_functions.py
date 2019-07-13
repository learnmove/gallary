# -*- coding: utf-8 -*-
import re
from net_tools import *

mainurl = 'https://www.ettoday.net/'

@exception
def newslist(soup_obj):
    result = findall(soup_obj,'h3')
    if not result:return
    for obj in result:
        type_ = find(obj,'em', class_="tag c_news")
        if type_:type_ = type_.text
        else:continue
        yield get_url(obj),type_

@exception
def get_url(soup_obj):#->str
    return mainurl + find(soup_obj,'a')['href']

@exception
def get_mtext(soup_obj):#->str
    result = ''
    for line in findall(soup_obj,'p'):
        txt = line.text
        if line.get('class') or re.search('[▲▼※]+|today',txt):
            continue
        if re.search('延伸閱讀|【.{2}新聞】|其他.+新聞|更多.*報導',txt):
            break
        for i in txt.split('\n'):
            if len(re.sub('\W+','',i)) < 20 and re.search('^記者|報導|^文／|^圖文',i):
                continue
            result += i + '\r\n'
    if not result:raise Exception('No mtext. as following as: ' + soup_obj.text)
    return result

def date_generator():
    now = time.time()
    newslist_url = mainurl + 'news/news-list-'
    while now:
        date = time.strftime("%Y-%m-%d-", time.localtime(now))
        daily_url = newslist_url + date
        for i in range(1,41):
            yield daily_url + str(i) + '.htm'
        now -= 86400
        
