# -*- coding: utf-8 -*-

import requests , bs4 , csv,re
bs = bs4.BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

url = 'https://www.coolpc.com.tw/evaluate.php'

soup = bs(requests.get(url,headers=headers).text,'html.parser')

def rule(text):
    check = ['$'] + ['機械','鍵盤'] # 你想要的條件，$為必要，不能刪
    for i in check:
        if not i in text:return
    anticheck = []  # 你不想要的條件，比如我找機械鍵盤不想要青軸，就輸入青軸
    for i in anticheck:
        if i in text:return
    return True

result = set()
for i in soup.find_all('option'):
    text = i.text
    if '共有' in text:
        for text in text.split('\n'):
            if rule(text):result.add(text)
    elif rule(text):result.add(text)


result = sorted(
    result,key = lambda x:int(
        re.findall('(?<=\$)\d+',x)[-1] 
        )) #依照價格排序，用findall再[-1]是因為有些項目的價格會像這樣: $1990↘$1799 那是優惠價，所以也要算上

with open('原價屋搜尋result.txt','w',newline='',encoding='utf-8-sig') as file:
    for i in result:
        file.write(i+'\r\n')
