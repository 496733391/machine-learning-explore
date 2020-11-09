#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path


data_df = pd.read_excel('C:/Users/Administrator/Desktop/报纸文献/1105光明日报文章链接知网.xlsx')
data_list = data_df.values.tolist()

count = 0
result_list = []
while count < len(data_list):
    try:
        for k in range(count, len(data_list)):
            print(k)
            data = data_list[k]
            url = data[-1]
            page = requests.get(url=url, headers=headers)
            soup = bs(page.text, 'lxml')
            keyword_t = soup.find(class_='keywords')
            if keyword_t:
                keyword = keyword_t.text
            else:
                keyword = ''
            abtext_t = soup.find(class_='abstract-text')
            if abtext_t:
                abtext = abtext_t.text
            else:
                abtext = ''
            page_name = re.findall(r'''<span class="rowtit">版名：</span><p>(.*?)</p>''', page.text)
            page_num = re.findall(r'''<span class="rowtit">版号：</span><p>(.*?)</p>''', page.text)
            k1 = re.findall(r'''<span class="rowtit">专辑：</span><p>(.*?)</p>''', page.text)
            k2 = re.findall(r'''<span class="rowtit">专题：</span><p>(.*?)</p>''', page.text)
            k3 = re.findall(r'''<span class="rowtit">分类号：</span><p>(.*?)</p>''', page.text)
            data += [keyword, abtext]
            if page_name:
                data += page_name
            else:
                data += ['']
            if page_num:
                data += page_num
            else:
                data += ['']
            if k1:
                data += k1
            else:
                data += ['']
            if k2:
                data += k2
            else:
                data += ['']
            if k3:
                data += k3
            else:
                data += ['']
            result_list.append(data)

        # 结束循环
        count = len(data_list)

    # 出现错误时，从错误处中断，再从该处开始
    except Exception as err:
        print('ERROR:%s' % err)
        print('当前进度：%s / %s' % (k, len(data_list)))
        count = k

result_df = pd.DataFrame(data=result_list, columns=['index_id', 'title', 'date', 'file_id', 'file_url', 'keyword', 'abstract', 'page_name', 'page_num', 'k1', 'k2', 'k3'])
result_df.to_excel('C:/Users/Administrator/Desktop/1105光明日报文章知网.xlsx', sheet_name='Sheet1', index=False)
