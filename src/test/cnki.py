#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.Scopus_Crawler.data_write import write2sql

date_list = [['2015-01-01', '2015-07-01'], ['2015-07-02', '2015-12-31'],
             ['2016-01-01', '2016-07-01'], ['2016-07-02', '2016-12-31'],
             ['2017-01-01', '2017-07-01'], ['2017-07-02', '2017-12-31'],
             ['2018-01-01', '2018-07-01'], ['2018-07-02', '2018-12-31'],
             ['2019-01-01', '2019-07-01'], ['2019-07-02', '2019-12-31']]

rmrb = '%E4%BA%BA%E6%B0%91%E6%97%A5%E6%8A%A5'
gmrb = '%E5%85%89%E6%98%8E%E6%97%A5%E6%8A%A5'
jjrb = '%E7%BB%8F%E6%B5%8E%E6%97%A5%E6%8A%A5'

headers['Content-Type'] = 'application/x-www-form-urlencoded'
post_url = 'https://kns.cnki.net/kns/request/SearchHandler.ashx'
# post_data = 'action=&NaviCode=*&ua=1.21&isinEn=0&PageName=ASP.brief_result_aspx&DbPrefix=CCND&DbCatalog' \
#             '=%e4%b8%ad%e5%9b%bd%e9%87%8d%e8%a6%81%e6%8a%a5%e7%ba%b8%e5%85%a8%e6%96%87%e6%95%b0%e6%8d%a' \
#             'e%e5%ba%93&ConfigFile=CCND.xml&db_opt=CCND&db_value=%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81' \
#             '%E6%8A%A5%E7%BA%B8%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93&magazine_value1=%E4%BA%BA%E6%B0%91%E6%97%A5%E6%8A%A5&magazine_special1=%3D' \
#             '&publishdate_from={}' \
#             '&publishdate_to={}' \
#             '&CKB_extension=ZYW&his=0&__=Wed%20Nov%2004%202020%2014%3A10%3A38%20GMT%2B0800%20' \
#             '(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'

post_data = 'action=&NaviCode=*&ua=1.21&isinEn=1&PageName=ASP.brief_result_aspx&DbPrefix=SCDB&DbCatalog' \
            '=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88' \
            '%e6%80%bb%e5%ba%93&ConfigFile=SCDB.xml&db_opt=CJFQ%2CCDFD%2CCMFD%2CCPFD%2CIPFD%2CCCND%2CCCJD' \
            '&magazine_value1=%E7%BB%8F%E6%B5%8E%E6%97%A5%E6%8A%A5' \
            '&magazine_special1=%25' \
            '&publishdate_from={}' \
            '&publishdate_to={}' \
            '&CKB_extension=ZYW&his=0&__=Thu%20Nov%2005%202020%2011%3A12%3A25%20GMT%2B0800%20(%E4' \
            '%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'

# get_url = 'https://kns.cnki.net/kns/brief/brief.aspx?curpage=%s&RecordsPerPage=50&QueryID=46&ID=&tur' \
#           'npage=1&tpagemode=L&dbPrefix=CCND&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=0&'

get_url = 'https://kns.cnki.net/kns/brief/brief.aspx?curpage=%s&RecordsPerPage=50&QueryID=14&ID=&turnpage=1' \
          '&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&'

result_list = []
for date in date_list:
    print(date)
    post_data_t = post_data.format(date[0], date[1])
    session = requests.session()
    session.post(url=post_url, data=post_data_t, proxies=proxies, headers=headers)

    page = session.get(url=get_url % '1', headers=headers, proxies=proxies)
    page_num_l = re.findall(r'''class='countPageMark'>1/(.*?)</span>''', page.text)
    session.close()
    page_num = int(page_num_l[0])
    print(page_num)
    count = 1
    while count < page_num+1:
        session = requests.session()
        session.post(url=post_url, data=post_data_t, proxies=proxies, headers=headers)
        try:
            for k in range(count, page_num+1):
                print(k)
                s_page = session.get(url=get_url % k, headers=headers, proxies=proxies, timeout=30)
                soup = bs(s_page.text, 'lxml')
                content = soup.find(class_='GridTableContent')
                content_list = content.find_all('tr')[1:]
                for c in content_list:
                    tds = c.find_all('td')
                    date = tds[4].text.strip()
                    title = tds[1].text.strip()
                    author_name = tds[2].text.strip()
                    author_link = re.findall(r'''href="(.*?)"''', '{}'.format(tds[2]))
                    article_link = re.findall(r'''href="(.*?)"''', '{}'.format(tds[1]))
                    author_link_str = ';'.join(author_link)
                    article_link_str = ';'.join(article_link)
                    result_list.append([title, date, article_link_str, author_name, author_link_str])
            # 结束循环
            count = page_num+1
            session.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            print('当前进度：%s / %s' % (k, page_num))
            count = k
            session.close()

data_df = pd.DataFrame(data=result_list, columns=['title', 'date', 'article_link', 'author_name', 'author_link'])
data_df.to_excel('C:/Users/Administrator/Desktop/1105知网经济日报.xlsx', sheet_name='Sheet1', index=False)

# file_base = 'https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CCND&dbname=CCNDLAST2015&filename='
# author_base = 'https://kns.cnki.net/kcms/detail/knetsearch.aspx?sfield=au&skey=%s&code=%s'
# data = pd.read_excel('C:/Users/Administrator/Desktop/1104知网光明日报.xlsx')
# data['index_id'] = data.index
# data['file_url'] = file_base + data['file_id']
# data.to_excel('C:/Users/Administrator/Desktop/1105光明日报文章链接知网.xlsx', sheet_name='Sheet1', index=False)
# author_list = []
# file_list = []
# for i in range(len(data)):
#     lis = data.loc[i, 'author_link'].split(';')
#     for li in lis:
#         if li != 'javascript:void(0)':
#             name = re.findall(r'''skey=(.*?)scode''', li)[0]
#             code = re.findall(r'''scode=(.*?)acode''', li)[0]
#             author_url = author_base % (name, code)
#             author_list.append(([data.loc[i, 'file_id'], data.loc[i, 'index_id'], code, author_url]))
#
# df = pd.DataFrame(data=author_list, columns=['file_id', 'index_id', 'code', 'author_url'])
# df.to_excel('C:/Users/Administrator/Desktop/1105光明日报作者链接知网.xlsx', sheet_name='Sheet1', index=False)
