#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path


data_df = pd.read_excel('C:/Users/Administrator/Desktop/1105光明日报作者链接知网.xlsx')
data_list = data_df.values.tolist()

count = 0
result_list = []
while count < len(data_list):
    try:
        for k in range(count, len(data_list)):
            print(k)
            url = data_list[k][-1]
            page = requests.get(url=url, headers=headers, proxies=proxies)
            ins = re.findall(r'''<h1 id="showname">.*?</h1>[\s\S]*?<h3><span><[\s\S]*?>([\s\S]*?)</a></span></h3>''', page.text)
            author_name = re.findall(r'''<h1 id="showname">(.*?)</h1>[\s\S]*?<h3><span><[\s\S]*?>[\s\S]*?</a></span></h3>''', page.text)
            if not ins:
                ins = ['']
            if not author_name:
                author_name = ['']
            result_list.append(data_list[k] + ins + author_name)
        # 结束循环
        count = len(data_list)

    # 出现错误时，从错误处中断，再从该处开始
    except Exception as err:
        print('ERROR:%s' % err)
        print('当前进度：%s / %s' % (k, len(data_list)))
        count = k

result_df = pd.DataFrame(data=result_list, columns=['file_id', 'index_id', 'code', 'author_url', 'ins', 'author_name'])
result_df.to_excel('C:/Users/Administrator/Desktop/1105光明日报作者知网.xlsx', sheet_name='Sheet1', index=False)
