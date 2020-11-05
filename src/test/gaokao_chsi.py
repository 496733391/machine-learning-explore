#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path

start_list = list(range(0, 2200, 20))
base_url = 'https://gaokao.chsi.com.cn/sch/search.do?searchType=1&xlcc=gzzk&start=%s'

result_list = []
for i, start in enumerate(start_list):
    print(i)
    url = base_url % start
    page = requests.get(url=url, headers=headers)
    soup = bs(page.text, 'lxml')
    content = soup.find(class_='ch-table')
    lis = content.find_all('tr')
    text_lis = [li.text.strip().replace('\r', '').replace('\n', '') for li in lis[1:]]
    for text in text_lis:
        tl = re.split(r'\s+', text)
        result_list.append(tl)

df = pd.DataFrame(data=result_list, columns=['院校', '院校所在地', '主管部门', '院校类型', '学历层次', '满意度'])
df.to_excel('C:/Users/Administrator/Desktop/1105专科院校.xlsx', sheet_name='Sheet1', index=False)

