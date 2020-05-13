#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from src.Scopus_Crawler.scopus_config import driver_path
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.authorID_get import get_id
from src.Scopus_Crawler.person_match import match

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
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        # 开始对每位学者再scopus上进行匹配和信息获取
        for i in range(count, len(input_data)):
            author_name = input_data[i]['name']
            author_ins = input_data[i]['ins']
            # 若是使用机构英文名称进行匹配，全部转为小写
            author_ins = [i.lower() for i in author_ins]
            authorID_list = get_id(driver, author_name, author_ins[0])
            author_id, doc_num, cite_count, institute_list = match(cookies, author_name, author_ins, authorID_list)


