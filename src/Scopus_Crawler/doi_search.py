#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from urllib.parse import quote
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.Scopus_Crawler.get_cookies import get_cookies


# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)
    return driver


def get_article_id(input_data):
    count = 0
    result_list = []
    no_search_result = []
    while count < len(input_data):
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        try:
            # 开始对每位学者再scopus上使用DOI搜索论文
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                doi = quote(input_data[i][2].strip().strip('.'), safe='.')
                url = "https://www.scopus.com/results/results.uri?sort=plf-f&src=s&st1=me&nlo=&nlr=&nls=&sot=b" \
                      "&sdt=b&sl=17&s=DOI%28{}%29".format(doi)
                doi_search_page = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
                soup = bs(doi_search_page.text, 'lxml')
                eid_element = soup.find(title=u'显示文献详情')
                if eid_element:
                    eid = eid_element['href']
                    result_list.append(input_data[i] + [eid])
                else:
                    print('未搜索到该论文: %s, %s' % (input_data[i][0], input_data[i][2]))
                    no_search_result.append(input_data[i])

            # 结束循环
            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

    result_df = pd.DataFrame(data=result_list, columns=['人才编号', '姓名', 'DOI', '署名', 'scopus论文ID'])
    no_search_result_df = pd.DataFrame(data=no_search_result, columns=['人才编号', '姓名', 'DOI', '署名'])
    no_search_result_df.to_excel('C:/Users/Administrator/Desktop/no_search_result_person0827.xlsx', sheet_name='Sheet1', index=False)
    result_df.to_excel('C:/Users/Administrator/Desktop/no_find_data0827.xlsx', sheet_name='Sheet1', index=False)


def get_author_id(input_data):
    count = 0
    result_list = []
    not_matched = []
    while count < len(input_data):
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        try:
            # 开始对每位学者发表论文的详细页,进行匹配
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                # url = "https://www.scopus.com/record/display.uri?eid={}&origin=resultslist".format(input_data[i][4])
                url = input_data[i][4]
                article_page = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
                sign_name = input_data[i][3].lower().replace(',', ' ').replace('.', ' ').replace('，', ' ').strip()
                sign_name_list = re.split(r'\s+|-', sign_name)
                sign_name_list = [ele for ele in sign_name_list if ele]
                sign_name_list += [element[0] for element in sign_name_list]
                soup = bs(article_page.text, 'lxml')
                element = soup.find(id='authorlist')
                author_list = element.find_all(title=u'显示作者详情')

                count = 0
                for author in author_list:
                    scopus_name = author.contents[0].contents[0].lower().strip('.').replace('-', '').replace('.', ', ').strip()
                    scopus_name_list = scopus_name.split(', ')
                    scopus_name_list += [element[0] for element in scopus_name_list]
                    if len(set(sign_name_list)) <= 2 or len(set(scopus_name_list)) <= 2:
                        if len(set(sign_name_list).intersection(set(scopus_name_list))) >= 2:
                            result_list.append([input_data[i][0], input_data[i][1], input_data[i][2],
                                                input_data[i][3], input_data[i][4], author['href'].split('&')[0]])
                            count += 1
                    else:
                        if len(set(sign_name_list).intersection(set(scopus_name_list))) >= 3:
                            result_list.append([input_data[i][0], input_data[i][1], input_data[i][2],
                                                input_data[i][3], input_data[i][4], author['href'].split('&')[0]])
                            count += 1

                if not count:
                    not_matched.append(input_data[i])

            # 结束循环
            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

    result_df = pd.DataFrame(data=result_list, columns=['人才编号', '姓名', 'DOI', '署名', 'scopus论文ID', 'scopus学者链接'])
    result_df.to_excel('C:/Users/Administrator/Desktop/no_find_result0827.xlsx', sheet_name='Sheet1', index=False)
    not_matched_df = pd.DataFrame(data=not_matched, columns=['人才编号', '姓名', 'DOI', '署名', 'scopus论文ID'])
    not_matched_df.to_excel('C:/Users/Administrator/Desktop/有论文未匹配上0827.xlsx', sheet_name='Sheet1', index=False)


if __name__ == '__main__':
    # first step
    df = pd.read_excel('C:/Users/Administrator/Desktop/马峥-学者DOI查找0729.xlsx')
    input_data = df.loc[df['署名'].notnull(), ['人才编号', '姓名', 'DOI', '署名']].values.tolist()
    get_article_id(input_data)

    # second step
    df2 = pd.read_excel('C:/Users/Administrator/Desktop/no_find_data0827.xlsx')
    input_data2 = df2.values.tolist()
    # input_data2 = input_data2[4:5]
    get_author_id(input_data2)
