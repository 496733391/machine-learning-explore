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
import random
import requests
import re

from src.Scopus_Crawler.scopus_config import driver_path, ins_url, headers, proxies, data_url
from src.Scopus_Crawler.get_cookies import get_cookies


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
                        'ins_id':[111, 222, 333], 'name_zh':'刘博'}, {...}]
    :return:
    '''
    person_id_list = list(set(input_data['person_id']))
    count = 0
    result_list = []
    while count < len(person_id_list):
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        try:
            # 开始对每位学者再scopus上进行匹配和信息获取
            for i in range(count, len(person_id_list)):
                print(i)
                temp_list = []
                for matched_id in list(input_data.loc[input_data['person_id'] == person_id_list[i]]['matched_id']):
                    url = ins_url % matched_id

                    passed_exp = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
                    ins_result = eval(passed_exp.text)
                    if len(ins_result) <= 40:
                        aff_df = pd.DataFrame(ins_result)
                        aff_df['scopus_person_id'] = matched_id
                        temp_list.append(aff_df)

                if temp_list:
                    temp_df = pd.concat(temp_list)
                    temp_df['person_id'] = person_id_list[i]
                    result_list.append(temp_df)

            # 结束循环
            count = len(person_id_list)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            print('当前进度：%s / %s' % (i + 1, len(person_id_list)))
            count = i

    return pd.concat(result_list)


if __name__ == '__main__':
    input_df = pd.read_excel('C:/Users/Administrator/Desktop/0701test.xlsx')
    source_data = pd.read_excel('C:/Users/Administrator/Desktop/人才名单_20200628.xlsx')
    source_data = source_data.loc[source_data['参考学科名称'].notnull(), ['人才编号', '参考学科名称']]
    source_data.drop_duplicates(subset=['人才编号'], inplace=True, ignore_index=True)

    result_df = main_prog(input_df)
    result_df = result_df.loc[:, ['person_id', 'scopus_person_id', 'affiliationName']]

    data_all = pd.read_excel('C:/Users/Administrator/Desktop/1-data20200628.xlsx')
    data_all.drop_duplicates(subset=['人才编号'], inplace=True, ignore_index=True)

    data_all['百度搜索链接'] = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' + data_all['当选单位名称'] + data_all['姓名']
    data_all['谷歌搜索链接'] = 'https://www.google.com/search?&q=' + data_all['当选单位名称'] + data_all['姓名']

    result_df = pd.merge(result_df, data_all, how='left', left_on='person_id', right_on='人才编号')
    result_df = pd.merge(result_df, source_data, how='left', on='人才编号')

    result_df.set_index(['person_id', '当选单位名称', '姓名', '百度搜索链接', '谷歌搜索链接', '参考学科名称', 'scopus_person_id', 'affiliationName'], inplace=True)
    result_df.to_excel('C:/Users/Administrator/Desktop/0701mult.xlsx', encoding='utf8')
