#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from selenium import webdriver
import pandas as pd
from selenium.webdriver import ChromeOptions
import datetime

from src.Scopus_Crawler.scopus_config import driver_path
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.authorID_get import get_id
from src.Scopus_Crawler.person_match import match
from src.Scopus_Crawler.data_write import write2sql, write2text
from src.config.logConfig import logger_scopus as logger

# 浏览器选项
options = ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)

    return driver


def main_prog(input_data):
    '''

    :param input_data: [{'name':'liu bo', 'ins':['fudan university', 'xx university', 'xxx university']}, {...}]
    :return:
    '''
    count = 0
    while count < len(input_data):
        all_aff_df = pd.DataFrame(data=None, columns=None)
        all_basic_info = []
        all_not_matched_one = []
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        try:
            # 开始对每位学者再scopus上进行匹配和信息获取
            for i in range(count, len(input_data)):
                author_name = input_data[i]['name']
                author_ins = input_data[i]['ins']
                # 若是使用机构英文名称进行匹配，全部转为小写
                author_ins = [i.lower() for i in author_ins]
                authorID_list = get_id(driver, author_name, author_ins[0])
                aff_df, basic_info, not_matched_one = match(cookies, author_name, author_ins, authorID_list)

                if basic_info:
                    all_aff_df = all_aff_df.append(aff_df, ignore_index=True)
                    all_basic_info.append(basic_info)

                else:
                    all_not_matched_one.append(not_matched_one)

            count = len(input_data)
            driver.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            logger.info('ERROR:%s' % err)
            logger.info('当前进度：%s / %s' % (i, len(input_data)))
            count = i
            driver.close()

        # 将已完成的部分进行数据写入
        basic_info_df = pd.DataFrame(data=all_basic_info, columns=['name', 'scopus_id', 'doc_num', 'cite_count'])
        write2sql([['author_info', basic_info_df], ['author_exp', all_aff_df]])
        write2text(all_not_matched_one)


if __name__ == '__main__':
    print(datetime.datetime.now())
    input_data = [{'name': 'Chen Jie', 'ins': ['Wuhan University', 'Université du Québec à Montréal', 'Université du Québec à Montréal']}]
    main_prog(input_data)
    print(datetime.datetime.now())
