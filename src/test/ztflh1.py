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
count = 15000
while count < 30000:
    try:
        for i in range(count, 30000):
            print(i)
            url = base_url % i
            page = requests.get(url=url, headers=headers)
            page.encoding = 'utf-8'
            code = re.findall(r'''<li><span class="code">(.*?)</span><a href=.*?>.*?</a></li>''', page.text)
            name = re.findall(r'''<li><span class="code">.*?</span><a href=.*?>(.*?)</a></li>''', page.text)
            code_list += code
            name_list += name

        # 结束循环
        count = 30000

    # 出现错误时，从错误处中断，再从该处开始
    except Exception as err:
        print('ERROR:%s' % err)
        print('当前进度：%s / %s' % (i, 30000))
        count = i

df = pd.DataFrame(data={'code': code_list, 'name': name_list})
df.to_excel('C:/Users/Administrator/Desktop/1106中图分类号1.xlsx', sheet_name='Sheet1', index=False)
