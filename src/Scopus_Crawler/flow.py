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
from src.Scopus_Crawler.data_write import write2sql
from src.config.logConfig import logger_scopus as logger
from src.Scopus_Crawler.data_process import data_process

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

    :param input_data: [{'person_id':1234564, 'name':'liu bo', 'ins':['fudan university', 'xx university', 'xxx university'],
                        'ins_id':[111, 222, 333]}, {...}]
    :return:
    '''
    count = 0
    while count < len(input_data):
        all_aff_df = pd.DataFrame(data=None, columns=None)
        all_basic_info = []
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        try:
            # 开始对每位学者再scopus上进行匹配和信息获取
            for i in range(count, len(input_data)):
                person_id = input_data[i]['person_id']
                author_name = input_data[i]['name']
                author_ins = input_data[i]['ins']
                author_ins_id = input_data[i]['ins_id']
                # 机构英文名称全部转为小写
                author_ins = [i.lower() for i in author_ins]
                authorID_list = get_id(driver, author_name, author_ins[0])
                # 以机构英文名称匹配
                # aff_df, basic_info = match(cookies, person_id, author_name, author_ins, authorID_list)
                # 以机构对应的scopus_id匹配
                aff_df, basic_info = match(cookies, person_id, author_name, author_ins_id, authorID_list)

                if basic_info:
                    all_aff_df = all_aff_df.append(aff_df, ignore_index=True)
                    all_basic_info.append(basic_info)

            count = len(input_data)
            driver.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            logger.info('ERROR:%s' % err)
            logger.info('当前进度：%s / %s' % (i, len(input_data)))
            count = i
            driver.close()

        # 将已完成的部分进行数据写入
        basic_info_df = pd.DataFrame(data=all_basic_info, columns=['person_id', 'name', 'scopus_id', 'doc_num', 'cite_count'])
        write2sql([['author_info', basic_info_df], ['author_exp', all_aff_df]])


if __name__ == '__main__':
    logger.info('********START********')
    # 测试用，从本地excel中读数据
    input_df = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data.xlsx')
    input_df.rename(columns={'学者代码': 'person_id',
                             '姓名': 'name',
                             '头衔当选单位': 'rankaff_name',
                             '软科代码': 'rankaff_id'}, inplace=True)

    input_data = data_process(input_df)

    input_data = input_data[12:20]

    main_prog(input_data)
