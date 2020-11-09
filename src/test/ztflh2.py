#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path

code_list = []
name_list = []
base_url = 'http://www.ztflh.com/?c=%s'
for i in range(30000, 45837):
    print(i)
    url = base_url % i
    page = requests.get(url=url, headers=headers)
    page.encoding = 'utf-8'
    code = re.findall(r'''<li><span class="code">(.*?)</span><a href=.*?>.*?</a></li>''', page.text)
    name = re.findall(r'''<li><span class="code">.*?</span><a href=.*?>(.*?)</a></li>''', page.text)
    code_list += code
    name_list += name

df = pd.DataFrame(data={'code': code_list, 'name': name_list})
df.to_excel('C:/Users/Administrator/Desktop/1106中图分类号2.xlsx', sheet_name='Sheet1', index=False)
