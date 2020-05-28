#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import json
from bs4 import BeautifulSoup as bs

url_base = 'https://www.scopus.com/authid/detail.uri?authorId=%s'

proxies = {"http": "http://202.120.43.93:8059"}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
           'e/81.0.4044.138 Safari/537.36'}

with open('C:/Users/Administrator/Desktop/machine-learning-explore/src/Scopus_Crawler/cookies.json', 'r') as f:
    cookies = json.load(f)

author_list = pd.read_excel('C:/Users/Administrator/Desktop/学者主要信息0528.xlsx', sheet_name='Sheet1')

lis = list(author_list['scopus学者代码'])

result_list = []
for i in lis:
    print(i)
    url = url_base % i
    page_source = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
    soup = bs(page_source.text, 'lxml')
    subject_area = soup.find(id='subjectAreaBadges')
    subject_list = subject_area.find_all(class_='badges')
    temp_lis = []
    for j in subject_list:
        temp_lis.append(j.text)
    result_list.append([i, ';'.join(temp_lis)])

result_df = pd.DataFrame(data=result_list, columns=['scopus学者代码', '学科领域'])
result_df.to_excel('C:/Users/Administrator/Desktop/学科领域信息0528.xlsx', index=False, encoding='utf-8')

