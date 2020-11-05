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

# data_df = pd.read_excel('C:/Users/Administrator/Desktop/1103光明日报.xlsx')
# data_list = data_df.values.tolist()
# result_list = []
# for k, data in enumerate(data_list):
#     print(k)
#     url = data[1]
#     page = requests.get(url, headers)
#     source = re.findall(r'''<span class="modbd"></span>[\s\S]*?<ul>[\s\S]*?</ul>[\s\S]*?<span class="modbd">''', page.text)
#     if source:
#         link_list = re.findall(r'''<li[\s\S]*?<a href=(.*?)>[\s\S]*?</a></li>''', source[0])
#         title_list = re.findall(r'''<li[\s\S]*?<a href=.*?>([\s\S]*?)</a></li>''', source[0])
#         domain_url = '/'.join(url.split('/')[:-1]) + '/'
#         link_list = [domain_url + i for i in link_list]
#         df = pd.DataFrame(data={'文章标题': title_list, '文章链接': link_list})
#         df['日期'] = data[2]
#         df['版面链接'] = data[1]
#         df['版面名称'] = data[0]
#         result_list.append(df)
#
# gmrb_ardf = pd.concat(result_list)
# gmrb_ardf.to_excel('C:/Users/Administrator/Desktop/1103光明日报文章链接.xlsx', sheet_name='Sheet1', index=False)

# data_df = pd.read_excel('C:/Users/Administrator/Desktop/1103光明日报文章链接.xlsx')
# data_list = data_df.values.tolist()
# count = 0
# while count < len(data_list):
#     result_list = []
#     try:
#         for i in range(count, len(data_list)):
#             print(i)
#             data = data_list[i]
#             url = data[1]
#             page = requests.get(url, headers)
#             author_info = re.findall(r'''<div class="lai">[\s\S]*?<span>(.*?)</span>''', page.text)
#             article_text = re.findall(r'''id="articleContent[\s\S]*?<!--enpcontent-->([\s\S]*?)<!--/enpcontent-->''', page.text)
#             if not author_info:
#                 author_info = ['']
#             if not article_text:
#                 article_text = ['']
#             data = data + author_info + article_text
#             result_list.append(data)
#
#         # 结束循环
#         count = len(data_list)
#
#     # 出现错误时，从错误处中断，再从该处开始
#     except Exception as err:
#         print('ERROR:%s' % err)
#         print('当前进度：%s / %s' % (i + 1, len(data_list)))
#         count = i
#
#     if result_list:
#         all_data_df = pd.DataFrame(data=result_list, columns=['text_title', 'text_link', 'text_date', 'page_name', 'au', 'all_text'])
#         write2sql([['gmrb_text', all_data_df]])

# dbutil = DBUtil(host, port, database, username, password)
# sql = 'select * from gmrb_text'
# data = dbutil.get_allresult(sql, 'df')
#
# data['单位'] = '0'
# for i in range(len(data)):
#     print(i)
#     data.loc[i, 'all_text'] = data.loc[i, 'all_text'][-300:]
#
# data.to_excel('C:/Users/Administrator/Desktop/1104光明日报.xlsx', index=False)

data = pd.read_excel('C:/Users/Administrator/Desktop/1104光明日报文章.xlsx')
data['单位'] = '0'
for i in range(len(data)):
    print(i)
    lis = re.split(r'''作者单位|作者为''', data.loc[i, 'all_text'])
    if len(lis) > 1:
        data.loc[i, '单位'] = lis[-1]

data.to_excel('C:/Users/Administrator/Desktop/1104光明日报.xlsx', index=False)
