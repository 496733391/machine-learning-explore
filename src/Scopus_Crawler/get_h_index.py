#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.data_write import write2sql


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


def crawl_h_index(input_data):
    count = 0
    while count < len(input_data):
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        result_list = []
        try:
            # 开始对每位学者再scopus上进行匹配和信息获取
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                url = 'https://www.scopus.com/authid/detail.uri?authorId=%s' % input_data[i][1]
                detail_page = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
                soup = bs(detail_page.text, 'lxml')
                h_index = soup.find(id='authorDetailsHindex')
                element = h_index.find(class_='fontLarge')
                if element:
                    result_list.append([input_data[i][0], input_data[i][1], element.text])

            # 结束循环
            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

        # 将已完成的部分进行数据写入
        result_df = pd.DataFrame(data=result_list, columns=['person_id', 'scopus_id', 'h_index'])
        write2sql([['h_index', result_df]])


if __name__ == '__main__':
    # 单元测试用
    dbutil = DBUtil(host, port, database, username, password)
    sql = 'select distinct person_id, scopus_id from author_info_new where ' \
          'person_id not in (select person_id from h_index)'
    author_id_df = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    input_data = author_id_df.values.tolist()
    crawl_h_index(input_data)
    print('****** END ******')
