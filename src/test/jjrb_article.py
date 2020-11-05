#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd

from src.Scopus_Crawler.data_write import write2sql
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
           'e/81.0.4044.138 Safari/537.36'}

# data_df = pd.read_excel('C:/Users/Administrator/Desktop/1103经济日报.xlsx')
# data_list = data_df.values.tolist()
# result_list = []
# for k, data in enumerate(data_list):
#     url = data[1]
#     page = requests.get(url, headers)
#     page.encoding = 'utf-8'
#     link_list = re.findall(r'''<td class=default valign="top"> <a href=(.*?)><div style="display:inline" id=.*?>.*?</div></a> </td>''', page.text)
#     title_list = re.findall(r'''<td class=default valign="top"> <a href=.*?><div style="display:inline" id=.*?>(.*?)</div></a> </td>''', page.text)
#     domain_url = '/'.join(url.split('/')[:-1]) + '/'
#     link_list = [domain_url + i for i in link_list]
#     df = pd.DataFrame(data={'文章标题': title_list, '文章链接': link_list})
#     df['日期'] = data[2]
#     df['版面链接'] = data[1]
#     df['版面名称'] = data[0]
#     result_list.append(df)
#
# jjrb_ardf = pd.concat(result_list)
# jjrb_ardf.to_excel('C:/Users/Administrator/Desktop/1103经济日报文章链接.xlsx', sheet_name='Sheet1', index=False)


data_df = pd.read_excel('C:/Users/Administrator/Desktop/1103经济日报文章链接.xlsx')
data_list = data_df.values.tolist()
result_list = []
for k, data in enumerate(data_list):
    print(k)
    url = data[1]
    page = requests.get(url, headers)
    page.encoding = 'utf-8'
    author_info = re.findall(r'''<td class=.*?align=center style="color: #827E7B;">(.*?)</td>''', page.text)
    article_text = re.findall(r'''<founder-content><P>([\s\S]*?)</P></founder-content>''', page.text)
    data = data + author_info + article_text
    result_list.append(data)

jjrb_ardf = pd.DataFrame(data=result_list, columns=['文章标题', '文章链接', '日期', '版面链接', '版面标题', 'au1', 'au2', '正文'])
jjrb_ardf.to_excel('C:/Users/Administrator/Desktop/1103经济日报文章.xlsx', sheet_name='Sheet1', index=False)
