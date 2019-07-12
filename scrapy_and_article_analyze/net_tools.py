# -*- coding: utf-8 -*-
import requests
from basic_tools import *
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

@exception
def session():#->session obj.
    return requests.Session()

@exception
def post(url,payload,req = requests):#->response obj.
    response = req.post(url, headers = headers,data = payload)
    response.raise_for_status()
    return response

@exception
def get(url,req = requests):#->response obj.
    response = req.get(url, headers = headers)
    response.raise_for_status()
    return response

@exception
def bs(response):#->BeautifulSoup obj.
    return BeautifulSoup(response.text,'html.parser')

@exception
def find(soup_obj,*args,**kwargs):#->BeautifulSoup obj.
    result = soup_obj.find(*args,**kwargs)
    if not result:
        raise Exception("Nobody has been found.")
    return result

@exception
def findall(soup_obj,*args,**kwargs):#->ResultSet
    result = soup_obj.find_all(*args,**kwargs)
    if not result:
        raise Exception("Nobody has been found.")
    return result
