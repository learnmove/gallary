# -*- coding: utf-8 -*-
import re
from net_tools import *

mainurl = 'https://www.mobile01.com/'

@exception
def get_url(soup_obj):#->str
    return mainurl + find(soup_obj,'a')['href']

@exception
def get_nextpage(soup_obj):#->str
    for i in findall(soup_obj,'a'):
        if i.text == '下一頁 ›.':
            return mainurl + i['href']

@exception
def get_mtext(soup_obj):#->str
    obj_to_string = soup_obj.__repr__()
    if 'blockquote' in obj_to_string:
        pattern = '<blockquote>.+?<\/blockquote>'
        result = re.sub(pattern,'',obj_to_string,re.S)
        result = re.sub('<.+?>','',result)
    else:result = soup_obj.text
    return result

@exception
def is_type(soup_obj):#->bool
    return soup_obj['class'][0] == "forumname"
