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
import time

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

# 学者详细页面地址
detail_base_url = 'https://www.scopus.com/authid/detail.uri?authorId=%s'
article_url = 'https://www.scopus.com/cto2/getdetails.uri?' \
              'ctoId=CTODS_%s' \
              '&stateKey=CTOF_%s' \
              '&startYear=2006&endYear=2020&docsPerPage=200&offset=%s' \
              '&usageKELogging=false&authorProfileOrigin=true&method=get'


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)
    return driver


def get_detail_data(input_data):
    data_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10, 99))
    count = 0
    while count < len(input_data):
        all_person_data_list = []
        driver = start_driver()
        try:
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                url = detail_base_url % input_data[i][1]
                driver.get(url)
                try:
                    driver.find_element_by_id('authViewCitOver').click()
                except Exception as err:
                    print('ERROR:%s' % err)
                    continue
                time.sleep(10)
                cto_id1 = re.findall(r'CTOF_([0-9]+)', driver.current_url)
                cto_id2 = re.findall(r'var ctoId = "CTODS_([0-9]+)"', driver.page_source)
                one_person_data_list = []
                # 页数循环
                for j in range(5):
                    url2 = article_url % (cto_id2[0], cto_id1[0], 200*j)
                    driver.get(url2)
                    if 'Error 500' in driver.page_source:
                        break
                    soup = bs(driver.page_source.replace('&nbsp;', '0'), 'lxml')
                    publish_year = re.findall(r'<span>([0-9]{4})</span>', driver.page_source)
                    previous_cell_count = [int(k.text) for k in soup.find_all(class_='previousCellCount')]
                    previous_years = [int(k.text) for k in soup.find_all(class_='previousYears')]
                    sub_total = [int(k.text) for k in soup.find_all(class_='subTotal')]
                    all_total = [int(k.text) for k in soup.find_all(class_='subtotal')]
                    prev_latest = [int(k.text) for k in soup.find_all(class_='prevLatestYears')]
                    one_page_data = pd.DataFrame({'publish_year': publish_year, 'previous_cell_count': previous_cell_count,
                                                  '2006': previous_years[0::15], '2007': previous_years[1::15],
                                                  '2008': previous_years[2::15], '2009': previous_years[3::15],
                                                  '2010': previous_years[4::15], '2011': previous_years[5::15],
                                                  '2012': previous_years[6::15], '2013': previous_years[7::15],
                                                  '2014': previous_years[8::15], '2015': previous_years[9::15],
                                                  '2016': previous_years[10::15], '2017': previous_years[11::15],
                                                  '2018': previous_years[12::15], '2019': previous_years[13::15],
                                                  '2020': previous_years[14::15], 'sub_total': sub_total,
                                                  'all_total': all_total, 'prev_latest': prev_latest})
                    one_person_data_list.append(one_page_data)

                if one_person_data_list:
                    one_person_data = pd.concat(one_person_data_list)
                    one_person_data['person_id'] = input_data[i][0]
                    one_person_data['scopus_id'] = input_data[i][1]
                    all_person_data_list.append(one_person_data)

            count = len(input_data)
            driver.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i
            driver.close()

        if all_person_data_list:
            all_person_data = pd.concat(all_person_data_list)
            all_person_data['article_num'] = 1
            final_data = all_person_data.groupby(by=['person_id', 'scopus_id', 'publish_year'], as_index=False).sum()
            final_data['data_no'] = data_no

            write2sql([['article_cite_data', final_data]])


if __name__ == '__main__':
    dbutil = DBUtil(host, port, database, username, password)
    sql = "select distinct person_id, scopus_id from author_info_new where person_id " \
          "not in (select person_id from article_cite_data where flag!=0) and person_id not in ('4179', '75', '6135', '5696', " \
          "'T2018002059') and flag!=0"
    df = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    input_data = df.values.tolist()
    get_detail_data(input_data)
