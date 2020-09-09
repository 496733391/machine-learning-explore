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
import datetime
import random

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.data_write import write2sql
from src.Scopus_Crawler.get_data import catch_info
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')

# 学者机构信息地址
ins_base_url = 'https://www.scopus.com/author/affilHistory.uri?auId=%s'
# 学者详细页面地址
detail_base_url = 'https://www.scopus.com/authid/detail.uri?authorId=%s'
# 学者文献及引证数据地址
data_base_url = 'https://www.scopus.com/author/highchart.uri?authorId=%s'


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)
    return driver


def get_detail_data(input_data):
    data_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10, 99))
    count = 0
    t_index = 4
    while count < len(input_data):
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        ins_data_list = []
        hindex_data_list = []
        article_data_list = []
        try:
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                # 获取学者文献及引证数据
                article_data_df = catch_info(input_data[i][t_index], cookies)
                article_data_df['name_zh'] = input_data[i][2]
                article_data_df['person_id'] = input_data[i][0]
                article_data_list.append(article_data_df)

                # 获取学者h_index数据
                detail_url = detail_base_url % input_data[i][t_index]
                detail_page = requests.get(detail_url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
                detail_soup = bs(detail_page.text, 'lxml')
                h_index = detail_soup.find(id='authorDetailsHindex')
                h_index_element = h_index.find(class_='fontLarge')
                if h_index_element:
                    hindex_data_list.append([input_data[i][0], input_data[i][t_index], h_index_element.text])

                # 获取学者机构数据
                ins_url = ins_base_url % input_data[i][t_index]
                ins_page = requests.get(ins_url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
                ins_data = eval(ins_page.text)
                for ins in ins_data:
                    # print(len(ins['affiliationName']), ins['affiliationName'])
                    ins['start_year'] = ins['dateRange'][0]
                    ins['end_year'] = ins['dateRange'][1]
                    ins.pop('dateRange')
                ins_data_df = pd.DataFrame(ins_data)
                rename_dict = {'affiliationCity': 'aff_city',
                               'affiliationName': 'aff_name',
                               'affiliationCountry': 'aff_country',
                               'affiliationId': 'aff_id',
                               'affiliationUrl': 'aff_url'}
                ins_data_df.rename(columns=rename_dict, inplace=True)
                ins_data_df['scopus_id'] = input_data[i][t_index]
                ins_data_df['person_id'] = input_data[i][0]
                ins_data_df['name_zh'] = input_data[i][2]
                ins_data_list.append(ins_data_df)

            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

        all_ins_data = pd.DataFrame() if not ins_data_list else pd.concat(ins_data_list)
        all_hindex_data = pd.DataFrame() if not ins_data_list else pd.DataFrame(data=hindex_data_list, columns=['person_id', 'scopus_id', 'h_index'])
        all_article_data = pd.DataFrame() if not ins_data_list else pd.concat(article_data_list)

        for _df in [all_ins_data, all_article_data]:
            if len(_df) > 0:
                _df['data_no'] = data_no
                _df['flag'] = 2

        all_hindex_data['flag'] = 2

        write2sql([['author_info_new', all_article_data], ['author_exp', all_ins_data],
                   ['h_index', all_hindex_data]])


if __name__ == '__main__':
    # dbutil = DBUtil(host, port, database, username, password)
    # sql = 'select distinct person_id from h_index'
    # author_id_df = dbutil.get_allresult(sql, 'df')
    # dbutil.close()

    df = pd.read_excel('C:/Users/Administrator/Desktop/已匹配scopusID.xlsx')
    df['person_id'] = df['person_id'].astype('str')
    input_data = df.values.tolist()
    get_detail_data(input_data)
